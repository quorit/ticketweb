const path = require("path")



const config_data = JSON.parse(process.env.VUE_APP_CONFIG_DATA);
const express = require("express")




module.exports = {

   parallel: false,

  transpileDependencies: [
    'vuetify'
  ],
  publicPath: config_data.vue_app_path_roots.app + "frontend/",
  // outputDir: path.resolve(process.env.VUE_APP_VENV_ROOT,"srv/ticketweb/applications/ithelp/frontend"),
  devServer: (process.env.NODE_ENV=='development')?{
    port: config_data.devel_port,
    proxy: {

         ['^' + config_data.vue_app_path_roots.authsystem]: {
            target: process.env.VUE_APP_BE_AUTHSYSTEM_URL,
            pathRewrite: {
               ['^' + config_data.vue_app_path_roots.authsystem]: '/'
            }
         },


         ['^' + config_data.vue_app_path_roots.app + "server/"]: {
            target: "http://127.0.0.1:"+process.env.VUE_APP_BE_PORT_NUMBER+"/",
            pathRewrite: {
               ['^' + config_data.vue_app_path_roots.app + "server/"]: '/'
            }
         },
         


   },
   setupMiddlewares: (middlewares, devServer) => {
      if (!devServer) {
        throw new Error('webpack-dev-server is not defined');
      }

      // Maps the URL path '/my-data' to a folder on your hard drive
      devServer.app.use(config_data.vue_app_path_roots.app + "shared-data/", express.static(process.env.VUE_APP_SYSTEM_DATA_DIR));
      
      return middlewares;
    }
  }:{}
  // options...
}
