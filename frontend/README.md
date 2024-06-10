## How to start

* Install node & npm
* Install ionic cli global: `npm install -g @ionic/cli`
* Run ionic project: `ionic serve`

## How to build the application for lndw
* Follow the setup instructions
* install the dependencies: `npm i`
* use the ionic serve option
  * run `ionic serve --prod --no-livereload`
* use one of the following
  * run `ionic build --prod`
  * run `cd www && npx http-server` or serve by any other webserver
