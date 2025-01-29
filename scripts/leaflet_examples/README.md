# Setting Up a Webpack + Leaflet Project with TypeScript

## Prerequisites
1. Install Node.js on your computer (if you don’t already have it) - [Download Node.js](https://nodejs.org/en/download)

## Project Setup
2. Create a folder for your project  
3. Open the folder in VS Code  
4. Open the terminal  

## Initialize Node and Webpack
5. Initialize the project with Node:  
   ```sh
   npm init
   ```
6. Fill out all the information to create a `package.json` file.  
7. Install Webpack:  
   ```sh
   npm install --save-dev webpack
   ```
8. Initialize Webpack:  
   ```sh
   npx webpack init
   ```
9. Install Webpack CLI generators (Command Line Interface to make life easier) by following the Webpack init prompt.  
10. You might need to initialize Webpack again after installing Webpack CLI generators:  
    ```sh
    npx webpack init
    ```

## Webpack Configuration Prompts
11. Follow the prompts:  
   - **JS Solution** = TypeScript  
   - **Webpack-dev-server** = Yes  
   - **Simplify creation of HTML files** = Yes (or your preference)  
   - **PWA support** = No  
   - **CSS Solution** = SASS  
   - **Use CSS styles along with SASS** = Yes  
   - **PostCSS** = No  
   - **Extract CSS for every file** = No  
   - **Prettier to format** = No  
   - **Package Manager** = NPM  
   - **Overwrite `package.json`** = Yes  

## Install Dependencies
12. Install Leaflet:  
    ```sh
    npm install leaflet
    ```
13. Install Esri Leaflet:  
    ```sh
    npm install esri-leaflet
    ```
14. Install Leaflet TypeScript definitions:  
    ```sh
    npm install --save-dev @types/leaflet
    ```
15. Install Esri Leaflet TypeScript definitions:  
    ```sh
    npm install --save-dev @types/esri-leaflet
    ```

## Development & Testing
16. Write your code/application (`TypeScript + HTML + SASS`).  
17. To compile and test:  
    ```sh
    npm run build
    ```
18. To test on a local server:  
    ```sh
    npm run serve
    ```