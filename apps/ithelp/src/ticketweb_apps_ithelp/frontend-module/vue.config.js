const path = require("path")



const config_data = JSON.parse(process.env.VUE_APP_CONFIG_DATA);
const express = require("express")




module.exports = {

   parallel: false,

  transpileDependencies: [
    'vuetify'
  ],
  publicPath: config_data.vue_app_path_roots.frontend,
  // outputDir: path.resolve(process.env.VUE_APP_VENV_ROOT,"srv/ticketweb/applications/ithelp/frontend"),
  devServer: (process.env.NODE_ENV=='development')?{
    port: config_data.devel_server.port,
    proxy: {

         ['^' + config_data.vue_app_path_roots.authsystem]: {
            target: config_data.devel_server.proxies.authsystem,
            pathRewrite: {
               ['^' + config_data.vue_app_path_roots.authsystem]: '/'
            }
         },


         ['^' + config_data.vue_app_path_roots.app_server]: {
            target: config_data.devel_server.proxies.app_server,
            pathRewrite: {
               ['^' + config_data.vue_app_path_roots.app_server]: '/'
            }
         },
         


   },
   setupMiddlewares: (middlewares, devServer) => {
      if (!devServer) {
        throw new Error('webpack-dev-server is not defined');
      }

      // Maps the URL path '/my-data' to a folder on your hard drive
      devServer.app.use(config_data.vue_app_path_roots.shared_data, express.static(process.env.VUE_APP_SYSTEM_DATA_DIR));
      
      return middlewares;
    }
  }:{}
  // options...
}
