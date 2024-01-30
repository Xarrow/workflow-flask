# -*- coding: utf-8 -*-
"""
Add New Function
"""

import time
import os
import asyncio
from pyppeteer import launch
dir_path = os.path.dirname(os.path.realpath(__file__))

ALL_SINGLE_FILE_JS_PATH =  f'{dir_path}/single-file-cli/lib/all-single-file.js'
SINGLE_FILE_JS =  f'{dir_path}/single-file-cli/lib/single-file.js'
SINGLE_FILE_BOOTSTRAP_JS = f'{dir_path}/single-file-cli/lib/single-file-bootstrap.js'
SINGLE_FILE_HOOK_FRAMES_JS = f'{dir_path}/single-file-cli/lib/single-file-hooks-frames.js'
SINGLE_FILE_ZIP_MIN_JS = f'{dir_path}/single-file-cli/lib/single-file-zip.min.js'
SCRIPTS = [
    SINGLE_FILE_JS,
    SINGLE_FILE_BOOTSTRAP_JS,
    SINGLE_FILE_HOOK_FRAMES_JS,
    SINGLE_FILE_ZIP_MIN_JS
]


class PySingleFileException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class GoToNewPageOption(object):
    def __init__(self,
                 url: str,
                 user_agent:str="",
                 wait_util:str ="networkidle0",
                 timeout: int = 7000,
                 wait_for_timeout:int = 7000,
                 cookies_list: list = None,
                 ) -> None:
        self.timeout = timeout
        self.user_agent = user_agent
        self.wait_for_timeout = wait_for_timeout
        self.wait_util = wait_util
        self.url = url
        self.cookies_list = cookies_list


class PySingleFile(object):
    def __init__(self, single_files_options:dict={}) -> None:
        self.pyppeteer_browser_options = {}
        self.browser = None
        self.page = None

        default_single_files_options = {
            "browserExecutablePath": "/usr/bin/google-chrome-stable",
            "dumpContent": True,
            "backEnd": "puppeteer",
            "acceptHeaders": {
                "font": "application/font-woff2;q=1.0,application/font-woff;q=0.9,*/*;q=0.8",
                "image": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
                "stylesheet": "text/css,*/*;q=0.1", "script": "*/*",
                "document": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"},
            "blockMixedContent": False,
            "browserServer": "",
            "browserHeadless": True,
            "browserWidth": 1440,
            "browserHeight": 900,
            "browserLoadMaxTime": 600000,
            "browserWaitDelay": 170000,
            "browserWaitUntil": "networkidle0",
            "browserWaitUntilFallback": True,
            "browserDebug": False,
            "browserArgs": "", 
            "browserStartMinimized": False,
            "browserCookiesFile": "",
            "browserIgnoreInsecureCerts": False, 
            "browserFreezePrototypes": False,
            "compressContent": False,
            "filenameTemplate": "%if-empty<{page-title}|No title> ({date-locale} {time-locale}).{filename-extension}",
            "filenameConflictAction": "uniquify",
            "filenameReplacementCharacter": "_",
            "filenameMaxLength": 192,
            "filenameMaxLengthUnit": "bytes", 
            "replaceEmojisInFilename": False,
            "groupDuplicateImages": True,
            "maxSizeDuplicateImages": 524288, 
            "httpProxyServer": "", 
            "httpProxyUsername": "",
            "httpProxyPassword": "", 
            "includeInfobar": False, 
            "insertMetaCsp": True,
            "loadDeferredImages": True,
            "loadDeferredImagesDispatchScrollEvent": False, "loadDeferredImagesMaxIdleTime": 1500,
            "loadDeferredImagesKeepZoomLevel": False, "loadDeferredImagesBeforeFrames": False,
            "maxParallelWorkers": 8, "maxResourceSizeEnabled": False, "maxResourceSize": 10,
            "moveStylesInHead": False,
            "outputDirectory": "", "password": "",
            "removeHiddenElements": True,
            "removeUnusedStyles": True, "removeUnusedFonts": True, "removeSavedDate": False,
            "removeFrames": False,
            "blockScripts": True, "blockAudios": True, "blockVideos": True,
            "removeAlternativeFonts": True,
            "removeAlternativeMedias": True, "removeAlternativeImages": True, "saveOriginalUrls": False,
            "saveRawPage": False, "webDriverExecutablePath": "", "userScriptEnabled": True,
            "crawlLinks": False,
            "crawlInnerLinksOnly": True, "crawlRemoveUrlFragment": True, "crawlMaxDepth": 1,
            "crawlExternalLinksMaxDepth": 1, "crawlReplaceUrls": False, "insertTextBody": False,
            "createRootDirectory": False,
            "selfExtractingArchive": True,
            "extractDataFromPage": True,
            "preventAppendedData": False,
            "url": None,
            "backgroundSave": True, "crawlReplaceURLs": False, "crawlRemoveURLFragment": True,
            "insertMetaCSP": True,
            "saveOriginalURLs": False,
            "httpHeaders": {},
            "browserCookies": [],
            "browserScripts": [],
            "browserStylesheets": [],
            "crawlRewriteRules": [], 
            "userAgent":None,
            "emulateMediaFeatures": []}
        default_single_files_options = default_single_files_options | single_files_options
        # pyppeteer browser options
        self.pyppeteer_browser_options = default_single_files_options
        self.pyppeteer_browser_options['executablePath'] = default_single_files_options['browserExecutablePath']
        self.pyppeteer_browser_options['headless'] = default_single_files_options.get('browserHeadless')
        self.pyppeteer_browser_options['ignoreHTTPSErrors'] = default_single_files_options.get('browserIgnoreInsecureCerts')
        self.pyppeteer_browser_options['args'] = [] if default_single_files_options.get(
            'browserArgs') is None or default_single_files_options.get('browserArgs') == '' else default_single_files_options.get(
            'browserArgs')

        self.pyppeteer_browser_options['width'] = default_single_files_options.get('browserWidth')
        self.pyppeteer_browser_options['height'] = default_single_files_options.get('browserHeight')

        # args
        self.pyppeteer_browser_options['args'].append('--disable-web-security')
        self.pyppeteer_browser_options['args'].append('--no-pings')
        self.pyppeteer_browser_options['args'].append('--no-sandbox')
        window_width = self.pyppeteer_browser_options.get("width")
        window_height = self.pyppeteer_browser_options.get("height")
        self.pyppeteer_browser_options['args'].append(f'--window-size={window_width}, {window_height}')
        if default_single_files_options.get('userAgent'):
            user_agent = default_single_files_options.get("userAgent")
            print(user_agent)
            self.pyppeteer_browser_options['args'].append(f'--user-agent={user_agent}')

        default_single_files_options['args'].append(
            f'--disable-extensions-except={"/workspaces/workflow-flask/single-file-cli/back-ends/extensions/bypass-csp"},{"/workspaces/workflow-flask/single-file-cli/back-ends/extensions/disable-web-security"},{"/workspaces/workflow-flask/single-file-cli/back-ends/extensions/network-idle"}')
        default_single_files_options['args'].append(
            f'--load-extension={"/workspaces/workflow-flask/single-file-cli/back-ends/extensions/bypass-csp"},{"/workspaces/workflow-flask/single-file-cli/back-ends/extensions/disable-web-security"},{"/workspaces/workflow-flask/single-file-cli/back-ends/extensions/network-idle"}')

        default_args = [
            '--disable-background-networking',
            '--enable-features=NetworkService,NetworkServiceInProcess',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-breakpad',
            '--disable-client-side-phishing-detection',
            '--disable-component-extensions-with-background-pages',
            '--disable-default-apps',
            '--disable-dev-shm-usage',
            '--disable-extensions',
            '--disable-features=TranslateUI,BlinkGenPropertyTrees',
            '--disable-hang-monitor',
            '--disable-ipc-flooding-protection',
            '--disable-popup-blocking',
            '--disable-prompt-on-repost',
            '--disable-renderer-backgrounding',
            '--disable-sync',
            '--force-color-profile=srgb',
            '--metrics-recording-only',
            '--no-first-run',
            '--enable-automation',
            '--password-store=basic',
            '--use-mock-keychain',
        ]

        for default_arg in default_args:
            default_single_files_options['args'].append(default_arg)

    async def start_browser(self,):
        try:
            self.browser = await launch(options=self.pyppeteer_browser_options)
            self.page =  await self.browser.newPage()
        except Exception as exception:
            raise PySingleFileException("Start browser failed", exception)

    async def load_sinlefile_js_config(self):
        if self.page is None:
            raise PySingleFileException("Start browser first")
        await self.page.setBypassCSP(False)
        await self.page.setExtraHTTPHeaders(self.pyppeteer_browser_options.get('httpHeaders'))
        await self.page.setViewport(
            {'width': self.pyppeteer_browser_options.get('browserWidth'),
             'height': self.pyppeteer_browser_options.get('browserHeight')}
        )
        script_tmp_zip = ""
        fr = open(SINGLE_FILE_ZIP_MIN_JS, mode='r')
        for line in fr:
            script_tmp_zip += line
        fr.close()
        self.pyppeteer_browser_options['zipScript'] = script_tmp_zip

        # 判断是否存在全部的 single-file js
        all_single_file_js=""
        if os.path.exists(ALL_SINGLE_FILE_JS_PATH):
            fr = open(ALL_SINGLE_FILE_JS_PATH,mode='r')
            for line in fr:
                all_single_file_js+=line
            fr.close()
        else:
            all_single_file_js = self._load_single_file_js_in_all()
            all_single_file_js = "()=>{" + all_single_file_js + "}"
            fw = open(ALL_SINGLE_FILE_JS_PATH,mode='w')
            fw.write(all_single_file_js)
            fw.flush()
            fw.close()

        await self.page.evaluateOnNewDocument(all_single_file_js)

    async def goto_new_page(self, goto_new_page_option: GoToNewPageOption):
        async def intercept(request):
                print(f'==>{request.method}-> {request.resourceType} | {request.url}')
                if "challenge-platform" in request.url:
                    await request.abort()
                if request.url.endswith('.png') or request.url.endswith('.jpg'):
                    await request.continue_()
                    # await request.abort()
                else:
                    await request.continue_()

        if self.page is None:
            raise PySingleFileException("Start browser first")
        if goto_new_page_option.user_agent:
            await self.page.setUserAgent(goto_new_page_option.user_agent)
        # cookies
        if goto_new_page_option.cookies_list:
            await self.page.setCookie(goto_new_page_option.cookies_list)
        try:
           await self.page.setRequestInterception(True)
           self.page.on('request', lambda req: asyncio.ensure_future(intercept(req)))

           await self.page.goto(url=goto_new_page_option.url,
                                 options={
                                     "waitUntil":
                                         goto_new_page_option.wait_util or
                                         self.pyppeteer_browser_options.get('browserWaitUntil'),
                                     "timeout":
                                         goto_new_page_option.timeout or
                                         self.pyppeteer_browser_options.get('browserLoadMaxTime'),
                                 })
           max_scrolls = 10000
           await self.page.evaluate('''
                async (maxScrolls, distance) => {
                    await new Promise((resolve) => {
                        var totalHeight = 0;
                        // scrolls counter
                        var scrolls = 0;
                        var timer = setInterval(() => {
                            var scrollHeight = document.body.scrollHeight;
                            window.scrollBy(0, distance);
                            totalHeight += distance;
                            // increment counter
                            scrolls++;
        
                            // stop scrolling if reached the end or the maximum number of scrolls
                            if (totalHeight >= scrollHeight - window.innerHeight || scrolls >= maxScrolls) {
                                clearInterval(timer);
                                resolve();
                            }
                        }, 1000);
                    })
                }
            ''', max_scrolls, 1000)
        except Exception as err:
            print(f'Url={goto_new_page_option.url} request timeout, stopLoading.')
            print(err)
            await self.page._client.send('Page.stopLoading')

        await self.page.waitFor(selectorOrFunctionOrTimeout=goto_new_page_option.wait_for_timeout)
        page_data = await self.page.evaluate('''
            async (options) => {
                return await singlefile.getPageData(options);
            }
        ''', self.pyppeteer_browser_options)
        return page_data

    async def close_browser(self, ):
        if self.browser:
            await self.browser.close()

    def _load_single_file_js_in_all(self):
        """
        加载 singleFiles js
        :return:
        """
        initSingleFileFunction = '''
            function initSingleFile() {
                singlefile.init({
                    fetch: (url, options) => {
                        return new Promise(function (resolve, reject) {
                            const xhrRequest = new XMLHttpRequest();
                            xhrRequest.withCredentials = true;
                            xhrRequest.responseType = "arraybuffer";
                            xhrRequest.onerror = event => reject(new Error(event.detail));
                            xhrRequest.onabort = () => reject(new Error("aborted"));
                            xhrRequest.onreadystatechange = () => {
                                if (xhrRequest.readyState == XMLHttpRequest.DONE) {
                                    resolve({
                                        arrayBuffer: async () => xhrRequest.response || new ArrayBuffer(),
                                        headers: { get: headerName => xhrRequest.getResponseHeader(headerName) },
                                        status: xhrRequest.status
                                    });
                                }
                            };
                            xhrRequest.open("GET", url, true);
                            if (options.headers) {
                                for (const entry of Object.entries(options.headers)) {
                                    xhrRequest.setRequestHeader(entry[0], entry[1]);
                                }
                            }
                            xhrRequest.send();
                        });
                    }
                });
            }
        '''
        scripts = "let _singleFileDefine; if (typeof define !== 'undefined') { _singleFileDefine = define; define = null }"
        for SCRIPT in SCRIPTS:
            with open(file=SCRIPT, mode="r", encoding="utf-8") as fr:
                scripts += fr.read() + "\n"
        # 自定义 js
        browserScripts = self.pyppeteer_browser_options.get('browserScripts')
        if browserScripts and len(browserScripts) > 0:
            for browserScript in browserScripts:
                with open(file=browserScript, mode="r", encoding="utf-8") as fr:
                    scripts += fr.read() + "\n"
        # 自定义 css
        browserStylesheets = self.pyppeteer_browser_options.get('browserStylesheets')
        if browserStylesheets and len(browserStylesheets) > 0:
            tmpStylesheets = ""
            for browserStylesheet in browserStylesheets:
                with open(file=browserStylesheet, mode="r", encoding="utf-8") as fr:
                    tmpStylesheets += fr.read()

            scripts += "addEventListener(\"load\",()=>{const styleElement=document.createElement(\"style\");styleElement.textContent=" + tmpStylesheets + ";document.body.appendChild(styleElement);});"

        browserFreezePrototypes = self.pyppeteer_browser_options.get('browserFreezePrototypes')
        if browserFreezePrototypes:
            scripts += "(true)();"
        else:
            scripts += "(false)();"
        scripts += "if (_singleFileDefine) { define = _singleFileDefine; _singleFileDefine = null }"

        scripts += "(" + initSingleFileFunction + ")();"
        return scripts

async def main():
    start_time  = time.time()
    pySingleFile = PySingleFile()
    await pySingleFile.start_browser()
    await pySingleFile.load_sinlefile_js_config()
    try:
        goToNewPageOption = GoToNewPageOption(url="https://twitter.com/",timeout=2000, wait_for_timeout=10000, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0")
        content = await pySingleFile.goto_new_page(goto_new_page_option=goToNewPageOption)
        print(content.get('filename'))
        c = content.get('content')
        fw = open(content.get('filename'), mode='w')
        fw.write(c)
        fw.flush()
        fw.close()
    except Exception as ex:
        print(ex)
    finally:
        await pySingleFile.close_browser()
        print(f'==> cost = {time.time()- start_time} ms')
    

asyncio.run(main())
    

        