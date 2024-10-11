#!/usr/bin/node
import { createQueue } from "kue";
const blacklistedNumbers = ['4153518780', '4153518781'];
const queue = createQueue();

const sendNotification = (phoneNumber, message, job, done) => {
    const total = 100;

    if (blacklistedNumbers.includes(phoneNumber)) {
        return done(new Error(`Phone number ${phoneNumber} is blacklisted`));
    }

    const next = (progress) => {
       if (progress === 0) {
            job.progress(progress, total);
       }
       if (progress === total /2) {
            job.progress(progress, total);
            console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
       }
       if (progress === total) {
            return done();
       } else {
            return next(progress + 1);
       }
    }

    // Call next function initially
    next(0);
};

queue.process('push_notification_code_2', 2, (job, done) => {
    sendNotification(job.data.phoneNumber, job.data.message, job, done);
});
