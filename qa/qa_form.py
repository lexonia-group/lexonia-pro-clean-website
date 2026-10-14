from playwright.sync_api import sync_playwright
BASE='http://127.0.0.1:8765/'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':850})
    errs=[]; pg.on('console',lambda m: errs.append(m.text[:140]) if m.type in('error','warning') else None)
    pg.goto(BASE+'contact.html')
    # validation: empty submit must be blocked
    pg.click('button[type=submit]'); pg.wait_for_timeout(300)
    print('blocked when empty:', pg.url.endswith('contact.html'), '| invalid fields:', pg.evaluate("[...document.querySelectorAll(':invalid')].map(e=>e.name)"))
    # honeypot not visible / not focusable
    print('honeypot hidden:', pg.evaluate("getComputedStyle(document.querySelector('[name=bot-field]').closest('p')).display"))
    # long input is capped
    pg.fill('#f-name','A'*500); print('name len capped:', len(pg.input_value('#f-name')))
    pg.fill('#f-message','B'*5000); print('message len capped:', len(pg.input_value('#f-message')))
    # XSS-looking input is submitted as data, never rendered
    pg.fill('#f-name','<img src=x onerror=alert(1)>'); pg.fill('#f-email','a@b.co'); pg.select_option('#f-service',index=1)
    pg.fill('#f-company','Test Co'); pg.fill('#f-phone','952-555-0100'); pg.fill('#f-size','5,000 sq ft'); pg.fill('#f-message','test')
    with pg.expect_navigation():
        pg.click('button[type=submit]')
    print('after submit url:', pg.url, '| h1:', pg.inner_text('h1')[:60])
    print('dialogs/errors:', errs)
    # honeypot filled => Netlify would drop it; check field name matches netlify-honeypot attr
    pg.goto(BASE+'contact.html'); print('honeypot attr:', pg.get_attribute('form','netlify-honeypot'), '| data-netlify:', pg.get_attribute('form','data-netlify'), '| form-name:', pg.get_attribute('input[name=form-name]','value'))
    b.close()
