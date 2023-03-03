const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/test',
    createProxyMiddleware({
      target: 'http://127.0.0.1:4999',
      changeOrigin: true,
    })
  );
};