// add the beginning of your app entry
import 'vite/modulepreload-polyfill'

import Alpine from 'alpinejs'
import htmx from 'htmx.org'

window.Alpine = Alpine
window.htmx = htmx

Alpine.start()
