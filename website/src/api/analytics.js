import api from './client'

const VISITOR_KEY = 'ss_visitor_uuid'
const SESSION_KEY = 'ss_session_uuid'

function uuid() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0
    const v = c === 'x' ? r : (r & 0x3) | 0x8
    return v.toString(16)
  })
}

function getVisitorId() {
  let id = localStorage.getItem(VISITOR_KEY)
  if (!id) {
    id = uuid()
    localStorage.setItem(VISITOR_KEY, id)
  }
  return id
}

function getSessionId() {
  let id = sessionStorage.getItem(SESSION_KEY)
  if (!id) {
    id = uuid()
    sessionStorage.setItem(SESSION_KEY, id)
  }
  return id
}

function getUtmParams() {
  const params = new URLSearchParams(window.location.search)
  return {
    utm_source: params.get('utm_source') || undefined,
    utm_medium: params.get('utm_medium') || undefined,
    utm_campaign: params.get('utm_campaign') || undefined,
    utm_term: params.get('utm_term') || undefined,
    utm_content: params.get('utm_content') || undefined,
  }
}

let sessionStarted = false

export function startSessionOnce() {
  if (sessionStarted) return
  sessionStarted = true
  const isNewSession = !sessionStorage.getItem(SESSION_KEY)
  const sessionId = getSessionId()
  if (!isNewSession) return

  api.post('/analytics/session', {
    visitor_uuid: getVisitorId(),
    session_uuid: sessionId,
    landing_page: window.location.pathname,
    referrer: document.referrer || undefined,
    browser: navigator.userAgent,
    device: /Mobi|Android/i.test(navigator.userAgent) ? 'mobile' : 'desktop',
    screen_width: window.screen.width,
    screen_height: window.screen.height,
    ...getUtmParams(),
  }).catch(() => {})
}

export function trackPageView(pageUrl) {
  api.post('/analytics/page-view', {
    session_uuid: getSessionId(),
    page_url: pageUrl,
  }).catch(() => {})
}

export function trackEvent(eventType, pageUrl, metadata) {
  api.post('/analytics/event', {
    session_uuid: getSessionId(),
    event_type: eventType,
    page_url: pageUrl || window.location.pathname,
    metadata_json: metadata || null,
  }).catch(() => {})
}
