#!/usr/bin/node
import { createQueue } from "kue";
import createPushNotificationsJobs from "./8-job";
import { expect } from "chai";
import sinon from 'sinon';


const queue = createQueue();

const jobsData = [
    {
      phoneNumber: '4153518780',
      message: 'This is the code 1234 to verify your account'
    },
    {
      phoneNumber: '4153518781',
      message: 'This is the code 4562 to verify your account'
    }
];

describe('createPushNotificationsJobs', () => {
    beforeEach(() => {
        sinon.spy(console, 'log');
    });

    before(() => {
        queue.testMode.enter();
    });

    afterEach(() => {
        sinon.restore();
        queue.testMode.clear();
    });

    after(() => {
        queue.testMode.exit();
    });

    it("should display an error if jobs is not an array", () => {
        expect(() => createPushNotificationsJobs(4, queue)).to.throw('Jobs is not an array');
    });

    it('should display an an error if queue is not a valid Kue', () => {
        expect(() => createPushNotificationsJobs(jobs, "")).to.throw();
    });

    it('should check enqueue event', (done) => {
        createPushNotificationsJobs(jobsData, queue);
        expect(queue.testMode.jobs.length).to.equal(2);
        expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3')
        expect(queue.testMode.jobs[0].data).to.eql(jobsData[0]);
        queue.testMode.jobs[0].on('enqueue', () => {
          const id = queue.testMode.jobs[0].id;
          expect(console.log.calledWith(`Notification job created: ${id}`)).to.be.true;
          done();
        });
      
        queue.testMode.jobs[0].emit('enqueue');
    });
    it('should check failed event', (done) => {
        createPushNotificationsJobs(jobsData, queue);
        queue.testMode.jobs[0].on('failed', () => {
          const id = queue.testMode.jobs[0].id;
          expect(console.log.calledWith(`Notification ${id} failed: job failed!`)).to.be.true;
          done();
        });
      
        queue.testMode.jobs[0].emit('failed', new Error('job failed!'));
    });

    it('should check complete event', (done) => {
        createPushNotificationsJobs(jobsData, queue);
        queue.testMode.jobs[0].on('complete', () => {
          const id = queue.testMode.jobs[0].id;
          expect(console.log.calledWith(`Notification job ${id} completed`)).to.be.true;
          done();
        });
      
        queue.testMode.jobs[0].emit('complete');
    });

    it('should check progress event', (done) => {
        createPushNotificationsJobs(jobsData, queue);
        queue.testMode.jobs[0].on('progress', () => {
          const id = queue.testMode.jobs[0].id;
          expect(console.log.calledWith(`Notification job ${id} 50% complete`)).to.be.true;
          done();
        });
      
        queue.testMode.jobs[0].emit('progress', 50);
    });
});
