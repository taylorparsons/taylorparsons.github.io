"""Security regressions for public metadata collection; no network required."""

import hashlib
import io
import tempfile
import unittest
import urllib.request
from email.message import Message
from pathlib import Path
from unittest import mock
from urllib.response import addinfourl

from defusedxml.common import DefusedXmlException

from scripts import collect_credits as collector

POM = """<project xmlns="http://maven.apache.org/POM/4.0.0">
  <url>https://example.org/project</url>
  <organization><name>Example maintainers</name></organization>
  <licenses><license><name>MIT</name></license></licenses>
  <dependencies><dependency>
    <groupId>org.example</groupId><artifactId>library</artifactId>
    <version>1.2.3</version>
  </dependency></dependencies>
</project>"""

UNSAFE_XML = (
    '<!DOCTYPE project [<!ENTITY value "expanded">]>'
    '<project>&value;</project>',
    '<!DOCTYPE project [<!ENTITY value SYSTEM "file:///etc/passwd">]>'
    '<project>&value;</project>',
    '<!DOCTYPE project SYSTEM "https://example.org/external.dtd">'
    '<project/>',
)


class CollectionSecurityTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.cache = Path(temporary.name) / 'cache'
        self.enterContext(mock.patch.object(collector, 'CACHE', self.cache))
        self.enterContext(mock.patch.object(collector, 'OFFLINE', False))

    def test_unsafe_urls_fail_before_cache_or_network_access(self):
        urls = (
            'file:///etc/passwd', 'http://example.org/metadata',
            'ftp://example.org/metadata', 'data:text/plain,metadata',
            'custom://example.org/metadata', '//example.org/metadata',
            'https:///metadata',
        )
        with mock.patch.object(collector.urllib.request, 'build_opener') as opener:
            for url in urls:
                with self.subTest(url=url), self.assertRaises(ValueError):
                    collector.get(url)
            opener.assert_not_called()
        self.assertFalse(self.cache.exists())

    def test_unsafe_url_is_rejected_even_when_cached(self):
        url = 'file:///etc/passwd'
        self.cache.mkdir()
        key = hashlib.sha256(url.encode()).hexdigest()
        (self.cache / key).write_text('old unsafe cache entry')
        with self.assertRaises(ValueError):
            collector.get(url)

    def test_https_cached_metadata_remains_available_offline(self):
        url = 'https://example.org/metadata'
        self.cache.mkdir()
        key = hashlib.sha256(url.encode()).hexdigest()
        (self.cache / key).write_text('{"cached": true}')
        with mock.patch.object(collector, 'OFFLINE', True):
            self.assertEqual(collector.get(url, as_json=True), {'cached': True})

    def test_offline_cache_miss_does_not_attempt_network(self):
        with mock.patch.object(collector, 'OFFLINE', True):
            with mock.patch.object(collector.urllib.request, 'build_opener') as opener:
                with self.assertRaises(FileNotFoundError):
                    collector.get('https://example.org/missing')
                opener.assert_not_called()

    def make_opener(self, redirect_target, status):
        """Use real urllib redirect processing with in-memory HTTP responses."""
        seen = []
        real_build_opener = urllib.request.build_opener

        class FixtureHTTPSHandler(urllib.request.HTTPSHandler):
            def https_open(self, request):
                seen.append(request.full_url)
                headers = Message()
                if len(seen) == 1:
                    headers['Location'] = redirect_target
                    code, body = status, b''
                else:
                    code, body = 200, b'{"downloaded": true}'
                response = addinfourl(io.BytesIO(body), headers, request.full_url, code)
                response.msg = 'fixture response'
                return response

        class DenyHTTPHandler(urllib.request.HTTPHandler):
            def http_open(self, request):
                raise AssertionError('An insecure HTTP target was opened')

        def factory(*handlers):
            return real_build_opener(*handlers, FixtureHTTPSHandler(), DenyHTTPHandler())

        return factory, seen

    def test_redirect_downgrades_are_blocked_for_all_supported_statuses(self):
        for status in (301, 302, 303, 307, 308):
            with self.subTest(status=status):
                factory, seen = self.make_opener('http://example.org/insecure', status)
                with mock.patch.object(collector.urllib.request, 'build_opener', factory):
                    with self.assertRaises(ValueError):
                        collector.get('https://example.org/redirect')
                self.assertEqual(seen, ['https://example.org/redirect'])
                self.assertEqual(list(self.cache.iterdir()), [])

    def test_other_unsafe_redirect_targets_are_rejected(self):
        request = urllib.request.Request('https://example.org/start')
        handler = collector.HTTPSRedirectHandler()
        for target in ('file:///etc/passwd', 'ftp://example.org/data', 'custom://host/data'):
            with self.subTest(target=target), self.assertRaises(ValueError):
                handler.redirect_request(request, None, 302, 'Found', {}, target)

    def test_https_redirect_downloads_and_caches_metadata(self):
        factory, seen = self.make_opener('https://example.org/final', 302)
        with mock.patch.object(collector.urllib.request, 'build_opener', factory):
            result = collector.get('https://example.org/start', as_json=True)
        self.assertEqual(result, {'downloaded': True})
        self.assertEqual(seen, ['https://example.org/start', 'https://example.org/final'])
        self.assertEqual(len(list(self.cache.iterdir())), 1)

    def test_normal_maven_source_dependencies_parse(self):
        entries = collector.parse_source({}, 'pom.xml', POM)
        self.assertEqual(entries, [{
            'ecosystem': 'maven', 'name': 'org.example:library',
            'version': '1.2.3', 'scope': 'declared', 'evidence': 'pom.xml',
        }])

    def test_normal_maven_attribution_parses(self):
        metadata = {'response': {'docs': [{'latestVersion': '1.2.3'}]}}
        with mock.patch.object(collector, 'get', side_effect=[metadata, POM]):
            record = collector.attribution('maven', 'org.example:library')
        self.assertNotIn('error', record)
        self.assertEqual(record['source'], 'https://example.org/project')
        self.assertEqual(record['maintainers'], ['Example maintainers'])
        self.assertEqual(record['license'], 'MIT')

    def test_source_xml_rejects_entities_and_external_dtds(self):
        for payload in UNSAFE_XML:
            with self.subTest(payload=payload), self.assertRaises(DefusedXmlException):
                collector.parse_source({}, 'pom.xml', payload)

    def test_metadata_xml_rejects_entities_and_preserves_error_reporting(self):
        metadata = {'response': {'docs': [{'latestVersion': '1.2.3'}]}}
        for payload in UNSAFE_XML:
            with self.subTest(payload=payload):
                with mock.patch.object(collector, 'get', side_effect=[metadata, payload]):
                    record = collector.attribution('maven', 'org.example:library')
                self.assertEqual(record['error'], 'DTDForbidden')
                self.assertEqual(record['maintainers'], [])

    def test_npm_alias_parsing_remains_supported(self):
        entries = collector.parse_source({}, 'package.json',
            '{"dependencies": {"alias": "npm:@example/library@^1.0"}}')
        self.assertEqual(entries[0]['name'], '@example/library')
        self.assertEqual(entries[0]['version'], '^1.0')


if __name__ == '__main__':
    unittest.main()
