const tf = require('@tensorflow/tfjs-node');
// const fs = require("fs");
const bodyPix = require('@tensorflow-models/body-pix');
const http = require('http');
const { Socket } = require('dgram');
const { buffer } = require('@tensorflow/tfjs-node');
const { type } = require('os');

(async () => {
    const net = await bodyPix.load({
        // architecture: 'MobileNetV1',
        // outputStride: 16,
        // multiplier: 0.50,
        // quantBytes: 1,
        architecture: 'MobileNetV1',
        outputStride: 16,
        multiplier: 0.75,
        quantBytes: 2
    });
    const server = http.createServer(function(req,res){
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.setHeader('Access-Control-Request-Method', '*');
        res.setHeader('Access-Control-Allow-Methods', 'OPTIONS, GET');
        res.setHeader('Access-Control-Allow-Headers', '*');
        if ( req.method === 'OPTIONS' ) {
            res.writeHead(200);
            res.end();
            return;
        }
    });

    server.on('request', async (req, res) => {

        var chunks = [];
        req.on('data', (chunk) => {
            chunks.push(chunk);
        });
        req.on('end', async () => {
            const image = tf.node.decodeImage(Buffer.concat(chunks));
            // fs.writeFile("out.png", Buffer.concat(chunks), 'base64', function(err) {
            //     console.log("error",err);
            //   });
            segmentation = await net.segmentPerson(image, {
                flipHorizontal: false,
                internalResolution: 'medium',
                segmentationThreshold: 0.7,
            });
            // const maskImage = bodyPix.toMask(segmentation,true)
            res.writeHead(200, { 'Content-Type': 'application/octet-stream' });
            res.write(Buffer.from(segmentation.data));
            res.end();
            tf.dispose(image);
        });
    });
    server.listen(8080);
})();


// socket.io

// // (async () => {
// var reservedRoom = 1
// const server = http.createServer(function(req,res){
//     res.setHeader('Access-Control-Allow-Origin', '*');
//     res.setHeader('Access-Control-Request-Method', '*');
//     res.setHeader('Access-Control-Allow-Methods', 'OPTIONS, GET');
//     res.setHeader('Access-Control-Allow-Headers', '*');
//     if ( req.method === 'OPTIONS' ) {
//         res.writeHead(200);
//         res.end();
//         return;
//     }
// });
// const io = require('socket.io')(server);


// io.on('connection', function (client) { 
//     var address = client.address;
//     // console.log("coonection established" , socket.)
//     console.log('New connection from ' + address);
//     // var chunks = [];
//     // req.on('data', (chunk) => {
//     //     chunks.push(chunk);
//     // });
//     client.emit('reservedRoom',String(reservedRoom))
//     reservedRoom += 1
//     client.on('frame', (frame,callback) => {
//         console.log("yeeees")
//         bodyPix.load({
//             architecture: 'MobileNetV1',
//             outputStride: 16,
//             multiplier: 0.75,
//             quantBytes: 2
//         }).then(net => perform(net)).catch(err => console.log(err))
//         console.log("yeeees1")
        
//         // const image = tf.node.decodeImage(frame);
//         // segmentation = await net.segmentPerson(image, {
//         //     flipHorizontal: false,
//         //     internalResolution: 'medium',
//         //     segmentationThreshold: 0.7,
//         // })
//         // // callback(Buffer.from segmentation.data)
//         // client.emit('processedFrame', Buffer.from(segmentation.data))
//         console.log('eh')
//     });

// });
// io.listen(8080);
// // })();
// async function perform(net) {
//     print("perform")
//     segmentation = await net.segmentPerson(image, {
//         flipHorizontal: false,
//         internalResolution: 'medium',
//         segmentationThreshold: 0.7,
//     })
//     return Buffer.from(segmentation.data)
// }
// function imageSegmentation(data){
//     (async () => {
//         const image = tf.node.decodeImage(Buffer.concat(data));
//         segmentation = await net.segmentPerson(image, {
//             flipHorizontal: false,
//             internalResolution: 'medium',
//             segmentationThreshold: 0.7,
//         });
//         return segmentation.data
//         // res.writeHead(200, { 'Content-Type': 'application/octet-stream' });
//         // res.write(Buffer.from(segmentation.data));
//         // res.end();
//         // tf.dispose(image);
//     });
// }