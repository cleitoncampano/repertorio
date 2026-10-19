import {defineConfig} from '@playwright/test';
export default defineConfig({
 testDir:'./e2e',fullyParallel:false,workers:1,timeout:30000,
 use:{baseURL:'http://127.0.0.1:8767',viewport:{width:1440,height:1000},trace:'retain-on-failure',launchOptions:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH?{executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH}:{}},
 webServer:{command:'../.venv/bin/python ../tests/e2e_server.py',url:'http://127.0.0.1:8767/api/health',reuseExistingServer:false,timeout:30000},
});
