module.exports = {
    collectCoverage: true,
    coverageReporters: ["cobertura"],
    watchAll: false,
    coverageThreshold: {
      global: {
        branches: 50,
        functions: 70,
        lines: 70,
        statements: 70
      }
    }
  };