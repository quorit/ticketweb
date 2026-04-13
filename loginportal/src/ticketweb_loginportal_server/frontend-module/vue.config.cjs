// vue.config.cjs

const path = require("path");

const config_data = JSON.parse(process.env.VUE_APP_CONFIG_DATA);




module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  publicPath: config_data.vue_app_path_root + "frontend/",
  devServer: (process.env.NODE_ENV=='development')?{
    port: config_data.devel_port,
    proxy: {
          
         ['^' + config_data.vue_app_path_root + "server/"]: {
            target: "http://127.0.0.1:"+process.env.VUE_APP_BE_PORT_NUMBER+"/",
            pathRewrite: {
               ['^' + config_data.vue_app_path_root + "server/"]: '/'
            }
         }


   }
  }:{}
  // options...
}
