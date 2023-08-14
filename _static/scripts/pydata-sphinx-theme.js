(()=>{"use strict";function e(e){"loading"!=document.readyState?e():document.addEventListener("DOMContentLoaded",e)}var t=window.matchMedia("(prefers-color-scheme: dark)");function o(e){document.documentElement.dataset.theme=t.matches?"dark":"light"}function n(e){"light"!==e&&"dark"!==e&&"auto"!==e&&(console.error(`Got invalid theme mode: ${e}. Resetting to auto.`),e="auto");var n=t.matches?"dark":"light";document.documentElement.dataset.mode=e;var r="auto"==e?n:e;document.documentElement.dataset.theme=r,localStorage.setItem("mode",e),localStorage.setItem("theme",r),console.log(`[PST]: Changed to ${e} mode using the ${r} theme.`),t.onchange="auto"==e?o:""}function r(){const e=document.documentElement.dataset.defaultMode||"auto",o=localStorage.getItem("mode")||e;var r,a;n(((a=(r=t.matches?["auto","light","dark"]:["auto","dark","light"]).indexOf(o)+1)===r.length&&(a=0),r[a]))}var a=()=>{let e=document.querySelectorAll("form.bd-search");return e.length?(1==e.length?e[0]:document.querySelector("div:not(.search-button__search-container) > form.bd-search")).querySelector("input"):void 0},c=()=>{let e=a(),t=document.querySelector(".search-button__wrapper");e===t.querySelector("input")&&t.classList.toggle("show"),document.activeElement===e?e.blur():(e.focus(),e.select(),e.scrollIntoView({block:"center"}))};function d(e){const t=`${DOCUMENTATION_OPTIONS.pagename}.html`,o=e.target.getAttribute("href");let n=o.replace(t,"");return fetch(o,{method:"HEAD"}).then((()=>{location.href=o})).catch((e=>{location.href=n})),!1}var l=document.querySelectorAll(".version-switcher__button");l.length&&fetch(DOCUMENTATION_OPTIONS.theme_switcher_json_url).then((e=>e.json())).then((e=>{const t=`${DOCUMENTATION_OPTIONS.pagename}.html`;l.forEach((e=>{e.dataset.activeVersionName="",e.dataset.activeVersion=""})),e.forEach((e=>{"name"in e||(e.name=e.version);const o=document.createElement("span");o.textContent=`${e.name}`;const n=document.createElement("a");n.setAttribute("class","list-group-item list-group-item-action py-1"),n.setAttribute("href",`${e.url}${t}`),n.appendChild(o),n.onclick=d,n.dataset.versionName=e.name,n.dataset.version=e.version,document.querySelector(".version-switcher__menu").append(n),"DOCUMENTATION_OPTIONS.version_switcher_version_match"==e.version&&(n.classList.add("active"),l.forEach((t=>{t.innerText=t.dataset.activeVersionName=e.name,t.dataset.activeVersion=e.version})))}))})),e((function(){n(document.documentElement.dataset.mode),document.querySelectorAll(".theme-switch-button").forEach((e=>{e.addEventListener("click",r)}))})),e((function(){if(!document.querySelector(".bd-docs-nav"))return;var e=document.querySelector("div.bd-sidebar");let t=parseInt(sessionStorage.getItem("sidebar-scroll-top"),10);if(isNaN(t)){var o=document.querySelector(".bd-docs-nav").querySelectorAll(".active");if(o.length>0){var n=o[o.length-1],r=n.getBoundingClientRect().y-e.getBoundingClientRect().y;if(n.getBoundingClientRect().y>.5*window.innerHeight){let t=.25;e.scrollTop=r-e.clientHeight*t,console.log("[PST]: Scrolled sidebar using last active link...")}}}else e.scrollTop=t,console.log("[PST]: Scrolled sidebar using stored browser position...");window.addEventListener("beforeunload",(()=>{sessionStorage.setItem("sidebar-scroll-top",e.scrollTop)}))})),e((function(){window.addEventListener("activate.bs.scrollspy",(function(){document.querySelectorAll(".bd-toc-nav a").forEach((e=>{e.parentElement.classList.remove("active")})),document.querySelectorAll(".bd-toc-nav a.active").forEach((e=>{e.parentElement.classList.add("active")}))}))})),e((function(){new MutationObserver(((e,t)=>{e.forEach((e=>{0!==e.addedNodes.length&&void 0!==e.addedNodes[0].data&&-1!=e.addedNodes[0].data.search("Inserted RTD Footer")&&e.addedNodes.forEach((e=>{document.getElementById("rtd-footer-container").append(e)}))}))})).observe(document.body,{childList:!0})}))})();
//# sourceMappingURL=pydata-sphinx-theme.js.map