const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    mode: 'development', // For production, use 'production' (is set to development for dev server to work properly)
    entry: {
        input: './src/input.ts',
        robot_socket: './src/robot_socket.ts',
        style: './src/style.css',
        robot_3d_plot: './src/robot3dplot.png',
    },
    devtool: 'inline-source-map',
    devServer: {
        static: './dist',
    },
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: 'ts-loader',
                exclude: /node_modules/,
            },
            {
                test: /\.css$/i,
                use: ['style-loader', 'css-loader'],
                exclude: /node_modules/,
            },
            {
                test: /\.(png|svg|jpg|jpeg|gif)$/i,
                type: 'asset/resource',
                exclude: /node_modules/,
            },
        ],
    },
    resolve: {
        extensions: ['.tsx', '.ts', '.js'],
    },
    output: {
        filename: '[name].js',
        path: path.resolve(__dirname, 'dist'),
        clean: true, // Clean the output directory before emit.
    },
    plugins: [
        new HtmlWebpackPlugin({ // Generate index.html based on src/index.html
            hash: true,
            template: './src/index.html',
            filename: './index.html' //relative to root of the application
        })
    ],
    optimization: {
        runtimeChunk: 'single',
    },
};