// Song: Cartoon - Howling (Ft. Asena)[NCS Release]
// Music provided by NoCopyrightSounds
// Free Download/Stream: http://ncs.io/Howling
// Watch: http://youtu.be/JiF3pbvR5G0

const fs = require('fs');
var amqp = require('amqplib/callback_api');

const config={
  protocol: 'amqp',
  hostname: 'localhost',
  port: 5672,
  username: 'merUser',
  password: 'passwordMER',
}

const GITHUB_WORKSPACE = process.env.GITHUB_WORKSPACE;
      qMain = 'lyrics',
      song = '{ "song": "Howling (Ft. Asena)", "artist": "Cartoon", "vID": "JiF3pbvR5G0" }',
      serv = '{"Service": "LyricsExtractor", "Result": {"vID": "JiF3pbvR5G0", "Filename": "JiF3pbvR5G0.txt"}}',
      qSec = 'management',
      file = 'JiF3pbvR5G0.txt';

describe('Testing RabbitMQ', ()=>{
  it('Should connect to the RabbitMQ', (done)=>{
    amqp.connect(config, (err, conn)=>{
      if(err){
        console.log("Connection Error");
        return;
      }
      done();
      setTimeout(function() { conn.close();}, 500);
    });
  });

  it('Should send a music to find genre', (done)=>{
    amqp.connect(config, (err, conn)=>{
      if(err){
        console.log("Connection Error");
        return;
      }
      conn.createChannel((err, ch)=>{
        if(err){
          console.log("Error Creating Channel");
          return;
        }
        ch.assertQueue(qMain, { durable: false }); 
        ch.sendToQueue(qMain, Buffer.from(song),
          function(err) {
            if(err) {
              console.log("Error sending the message: ",err);
              return;         
            } else {
              console.log("Message sent");
              done();
          }
        });
      });
      done();
      setTimeout(function() { conn.close();}, 500);
    });
  });

  it('Should create the RabbitMQ channel', (done)=>{
    amqp.connect(config, (err, conn)=>{
      if(err){
        console.log("Connection Error");
        return;
      }
      conn.createConfirmChannel((err, ch)=>{
        if(err){
          console.log("Error Creating Channel");
          return;
        }
        done();
        setTimeout(function() { conn.close();}, 500);
      });
    });
  });

  it('Should split the music', function(done) {
    setTimeout(function(){
      fs.access(`${GITHUB_WORKSPACE}/JiF3pbvR5G0/${file}`, fs.F_OK, (err) => {
        if (err) {
          console.error(err)
          console.log("File not found!");
          return
        }
        console.log("File found!");
        done();
      })}, 4000);
  });

  // it("Should receive the genre from RabbitMQ", (done)=>{
  //   amqp.connect(config, (err, conn)=>{
  //     if(err){
  //       console.log("Connection Error");
  //       return;
  //     }
  //     conn.createChannel( (err, ch)=>{
  //       if(err){
  //         console.log("Error Creating Channel");
  //         return;
  //       }
  //       ch.assertQueue(qSec, { durable: false });
  //       ch.consume(qSec, function (msg) {
  //         if (JSON.stringify(msg.content.toString()) === JSON.stringify(serv)){
  //           done();
  //           setTimeout(function() { conn.close();}, 500);
  //         } else {
  //           console.log("Unexpected message");
  //           return;
  //         }
  //       }, { noAck: true });
  //     });
  //   });
  // });
});