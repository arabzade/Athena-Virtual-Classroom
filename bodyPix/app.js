const tf = require('@tensorflow/tfjs-node');
const fs = require("fs");
const bodyPix = require('@tensorflow-models/body-pix');
const http = require('http');
(async () => {
    const net = await bodyPix.load({
        architecture: 'MobileNetV1',
        outputStride: 16,
        multiplier: 0.75,
        quantBytes: 2,
    });
    const server = http.createServer();
    server.on('request', async (req, res) => {
        var chunks = [];
        req.on('data', (chunk) => {
            chunks.push(chunk);
        });
        req.on('end', async () => {
            const image = tf.node.decodeImage(Buffer.concat(chunks));
            fs.writeFile("out.png", Buffer.concat(chunks), 'base64', function(err) {
                console.log("error",err);
              });
            segmentation = await net.segmentPerson(image, {
                flipHorizontal: false,
                internalResolution: 'medium',
                segmentationThreshold: 0.7,
            });
            // const maskImage = bodyPix.toMask(segmentation,true)
            // console.log(maskImage)          
            res.writeHead(200, { 'Content-Type': 'application/octet-stream' });
            fs.writeFile("out1.png", Buffer.from(segmentation.data), 'base64', function(err) {
                console.log("error",err);
              });
            res.write(Buffer.from(segmentation.data));
            res.end();
            tf.dispose(image);
        });
    });
    server.listen(8080);
})();