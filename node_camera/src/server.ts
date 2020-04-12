import bodyParser from "body-parser";
import cors from "cors";
import express, { Express, Request, Response, Router } from "express";
const rateLimit = require("express-rate-limit");
import fs from "fs";
import http from "http";
import https from "https";
import path from "path";
import { Codec, Rotation, SensorMode, StillCamera, StreamCamera } from "pi-camera-connect";


let port = 80;

if (fs.existsSync("./isDev")) port = 8000;

const app = express();
// Cors
app.use(cors());
app.use(function (req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
});

// bodyparser
app.use(bodyParser.urlencoded({
    extended: false,
}));
app.use(bodyParser.text());
app.use(bodyParser.json());



// enable rate limiter
const apiLimiter = rateLimit({
    windowMs: 1 * 60 * 1000,
    max: 100,
});
app.use("/api/", apiLimiter);


// Define Express routes
app.use("/", express.static(path.join(__dirname, "www")));


const router = Router();

router.get("/api/cam", (req: Request, res: Response) => {
    console.log("API CAM");
    const streamCamera = new StreamCamera({
        codec: Codec.MJPEG,
        width: 1280,
        height: 720,
        fps: 30,
        rotation: Rotation.Rotate90,
    });

    const videoStream = streamCamera.createStream();
    const head = {
        "Content-Type": "image/jpeg",
        };
    res.writeHead(200, head);

    videoStream.pipe(res);

    streamCamera.startCapture().then(() => {
        console.log("stream start capture");
        streamCamera.stopCapture();
    });
});

app.use(router);

http.createServer({}, app).listen(port, () => {
    console.log("SERVER", " started at https://localhost:", port);
});


// const stillCamera = new StillCamera({
//     width: 1280,
//     height: 720,
// });

// stillCamera.takeImage()
// .then((image) => {
//     let imagePath = path.join(__dirname, "www/still-image.jpg");
//     fs.writeFileSync(imagePath, image);
// });
