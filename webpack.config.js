//webpack.config.js
const path = require('path');
const {merge} = require('webpack-merge');

const defaultConfig = {
  resolve: {
    extensions: ['.ts', '.tsx', '.js'],
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        loader: 'ts-loader',
      },
    ],
  },
};

const baseConfig = {
  entry: {
    main: './src/base.ts',
  },
  output: {
    path: path.resolve(__dirname, './app/static'),
    filename: 'js/base.js', // <--- Will be compiled to this single file
  },
};

const userConfig = {
  entry: {
    main: './src/user.ts',
  },
  output: {
    path: path.resolve(__dirname, './app/static'),
    filename: 'js/user.js', // <--- Will be compiled to this single file
  },
};

const pestConfig = {
  entry: {
    main: './src/pest.ts',
  },
  output: {
    path: path.resolve(__dirname, './app/static'),
    filename: 'js/pest.js', // <--- Will be compiled to this single file
  },
};

const slideShowConfig = {
  entry: {
    main: './src/slideshow.ts',
  },
  output: {
    path: path.resolve(__dirname, './app/static'),
    filename: 'js/slideshow.js', // <--- Will be compiled to this single file
  },
};

const configs = [baseConfig, userConfig, pestConfig, slideShowConfig].map(conf =>
  merge(defaultConfig, conf),
);

module.exports = configs;
