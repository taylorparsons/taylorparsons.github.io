export default [
  {
    files: ["assets/**/*.js"],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "script",
      globals: {
        document: "readonly",
        navigator: "readonly",
        setTimeout: "readonly",
      },
    },
    rules: {
      "no-undef": "error",
      "no-unused-vars": "error",
      "no-unreachable": "error",
      "constructor-super": "error",
      "valid-typeof": "error",
    },
  },
];
