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

# Styling
Jede Komponente hat ihr eigenes jeweiliges Styling im jeweiligen Ordner der Komponente, [siehe](src\app\home\home.page.scss) zum Beispiel. 
Anpassungen für die Searchbars und dem large viewport wurden jedoch in der [global.scss](src\global.scss) getroffen.
Des weiteren sind die einzelnen Farben und auch andere Variablen in der [variables.scss](src\theme\variables.scss) festgehalten.
Die hauptsächlich verwendeten Farben der Anwendung enthalten dabei --ion-color-custom-* im Namen und sind abgestimmt mit dem Titelbild, welches zu der Home Komponente gehört.

## Verwendete Bilder
Alle verwendeten Bilder sind KI generiert. Das Bild der Home Komponente wurde dabei mit dem Microsoft AI Image Generator, [siehe](https://create.microsoft.com/en-us/features/ai-image-generator), generiert und anschließend entsprechend der Bedürfnisse angepasst.
Die anderen Bilder wurden mit dem Ai Generator von deepai generiert [siehe](https://deepai.org/machine-learning-model/text2img)

Ein Bild mit den entsprechenden Einstellungen zur Erhaltung des selben Stils, befindet sich [hier](src\theme\Image.PNG)
*Dabei ist zu beachten dass gegebenenfalls mehrmals generiert werden muss bis der gewünschte Stil erreicht wird.*
