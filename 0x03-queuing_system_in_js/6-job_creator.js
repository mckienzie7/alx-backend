#!/usr/bin/node
import { createQueue } from "kue";

const queue = createQueue();

const job = queue.create("push_notification_code", {
    phoneNumber: "+254712345678",
    message: "Account created successfully",
}).save((err) => {
    if( !err ) console.log(`Notification job created: ${job.id}`);
 });;

 job.on('complete', () => {
    console.log(`Notification job completed`);
  });

  job.on('failed', () => {
    console.log('Job failed');
  });
