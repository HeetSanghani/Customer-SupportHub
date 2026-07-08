/* ============================================================
   SupportHub — AI Omnichannel Customer Support Platform
   Clickable static frontend prototype. No backend / no APIs.
   ============================================================ */

/* ---------------- Icons (inline SVG, line style) ---------------- */
const ICN = {
  home:'<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V20a1 1 0 0 0 1 1h4v-6h4v6h4a1 1 0 0 0 1-1V9.5"/>',
  ticket:'<path d="M3 8a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v2a2 2 0 0 0 0 4v2a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-2a2 2 0 0 0 0-4Z"/><path d="M9 7v10" stroke-dasharray="2 2"/>',
  chat:'<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5Z"/>',
  bot:'<rect x="4" y="8" width="16" height="12" rx="3"/><circle cx="9" cy="14" r="1.4"/><circle cx="15" cy="14" r="1.4"/><path d="M12 8V4"/><circle cx="12" cy="3" r="1.2"/><path d="M2 13h2M20 13h2"/>',
  book:'<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5v-15Z"/><path d="M4 20.5A2.5 2.5 0 0 1 6.5 18H20"/>',
  user:'<circle cx="12" cy="8" r="3.6"/><path d="M4.5 20.5a7.5 7.5 0 0 1 15 0"/>',
  inbox:'<path d="M3 12h4.5l1.5 3h6l1.5-3H21"/><path d="M5 5h14l2 7v6a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 3 18v-6l2-7Z"/>',
  list:'<path d="M8 6h13M8 12h13M8 18h13"/><circle cx="3.5" cy="6" r="1"/><circle cx="3.5" cy="12" r="1"/><circle cx="3.5" cy="18" r="1"/>',
  users:'<circle cx="9" cy="8" r="3.2"/><path d="M2.7 19.5a6.3 6.3 0 0 1 12.6 0"/><path d="M16 5.2A3.2 3.2 0 0 1 16.9 11.5"/><path d="M17.5 14.2a6.3 6.3 0 0 1 3.8 5.3"/>',
  alert:'<path d="M10.3 3.9 2.6 18a1.5 1.5 0 0 0 1.3 2.2h16.2a1.5 1.5 0 0 0 1.3-2.2L13.7 3.9a1.5 1.5 0 0 0-2.6 0Z"/><path d="M12 9.5v4M12 16.7h.01"/>',
  smile:'<circle cx="12" cy="12" r="9"/><path d="M8 14s1.5 2 4 2 4-2 4-2M9 9h.01M15 9h.01"/>',
  chart:'<path d="M4 20V10M11 20V4M18 20v-7"/><path d="M3 20h18"/>',
  gear:'<circle cx="12" cy="12" r="3"/><path d="M19.4 13.5a7.6 7.6 0 0 0 0-3l2-1.5-2-3.5-2.4.7a7.6 7.6 0 0 0-2.6-1.5L14 2h-4l-.4 2.7a7.6 7.6 0 0 0-2.6 1.5l-2.4-.7-2 3.5 2 1.5a7.6 7.6 0 0 0 0 3l-2 1.5 2 3.5 2.4-.7a7.6 7.6 0 0 0 2.6 1.5L10 22h4l.4-2.7a7.6 7.6 0 0 0 2.6-1.5l2.4.7 2-3.5Z"/>',
  shield:'<path d="M12 2.5 4.5 5.5v6c0 5 3.2 8.4 7.5 10 4.3-1.6 7.5-5 7.5-10v-6L12 2.5Z"/><path d="M9 12l2 2 4-4.2"/>',
  plug:'<path d="M9 3v5M15 3v5M6 8h12l-1 5a5 5 0 0 1-10 0L6 8Z"/><path d="M12 17.5V21"/>',
  sliders:'<path d="M4 6h9M17 6h3M4 12h3M9 12h11M4 18h13M19 18h1"/><circle cx="15" cy="6" r="1.8"/><circle cx="7" cy="12" r="1.8"/><circle cx="17" cy="18" r="1.8"/>',
  search:'<circle cx="11" cy="11" r="7"/><path d="m21 21-4.35-4.35"/>',
  bell:'<path d="M18 9.5a6 6 0 0 0-12 0c0 5.3-2 6.5-2 6.5h16s-2-1.2-2-6.5Z"/><path d="M9.5 19a2.5 2.5 0 0 0 5 0"/>',
  chev:'<path d="m9 6 6 6-6 6"/>',
  check:'<path d="m5 12 5 5 9-9"/>',
  clock:'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
  send:'<path d="m3 11 18-8-8 18-2.5-7.5L3 11Z"/>',
  sparkle:'<path d="M12 3v3M12 18v3M3 12h3M18 12h3M6 6l1.8 1.8M16.2 16.2 18 18M6 18l1.8-1.8M16.2 7.8 18 6"/><path d="M12 9.5 13 12l2.5 1-2.5 1-1 2.5-1-2.5L8.5 13l2.5-1Z"/>',
  mail:'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6 8.5 7 8.5-7"/>',
  star:'<path d="m12 2.5 2.9 5.9 6.5.9-4.7 4.6 1.1 6.4L12 17.3l-5.8 3 1.1-6.4L2.6 9.3l6.5-.9L12 2.5Z"/>',
  arrowUp:'<path d="M6 15 12 9l6 6"/>',
  arrowDown:'<path d="M6 9 12 15l6-6"/>',
  logout:'<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><path d="M16 17l5-5-5-5"/><path d="M21 12H9"/>',
  grid:'<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
  filter:'<path d="M4 5h16l-6 8v6l-4-2v-4L4 5Z"/>',
  plus:'<path d="M12 5v14M5 12h14"/>',
  phone:'<path d="M6.5 3h3l1.5 5-2.5 1.5a13 13 0 0 0 5 5L15 12l5 1.5v3a2 2 0 0 1-2.2 2A17 17 0 0 1 4.5 5.2 2 2 0 0 1 6.5 3Z"/>',
  whatsapp:'<path d="M6 18.5 3.5 21l2.5-2.5A8.5 8.5 0 1 1 20.5 12 8.5 8.5 0 0 1 6 18.5Z"/><path d="M8.5 9.2c0 4 3.3 6.3 6.3 6.3.7 0 1.7-.6 1.8-1.3l-2.4-1.4-1 .9c-1-.5-2.1-1.6-2.6-2.6l.9-1-1.4-2.4c-.7.1-1.6.9-1.6 1.5Z"/>',
  instagram:'<rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17" cy="7" r="1"/>',
  facebook:'<path d="M14 21v-7h2.5l.5-3H14V9c0-.9.3-1.5 1.7-1.5H17V4.8C16.6 4.7 15.6 4.5 14.4 4.5 11.9 4.5 10 6 10 8.7V11H7.5v3H10v7Z"/>',
  globe:'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
  paperclip:'<path d="M8 12.5 15 5.5a3.5 3.5 0 0 1 5 5l-8.5 8.5a5.5 5.5 0 1 1-7.8-7.8L12 3"/>',
  refresh:'<path d="M4 4v5h5"/><path d="M20 20v-5h-5"/><path d="M4.6 15a8 8 0 0 0 14.8 1.5M19.4 9a8 8 0 0 0-14.8-1.5"/>',
  download:'<path d="M12 3v13M7 11l5 5 5-5"/><path d="M4 19h16"/>',
  building:'<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M9 8h1M14 8h1M9 12h1M14 12h1M9 16h1M14 16h1"/>',
  key:'<circle cx="8" cy="15" r="4"/><path d="M11 12 19 4"/><path d="M16 7l2.5 2.5M19 4l2 2"/>',
};
function icon(name, size=18, cls=''){
  return `<svg class="${cls}" width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${ICN[name]||''}</svg>`;
}

/* ---------------- Static demo data ---------------- */
const AGENTS = [
  {id:'emma', name:'Emma Wilson', title:'Senior Support Agent', initials:'EW', color:'#4F46E5', tickets:14, csat:4.8, sla:97, resolved:212, avgHandle:'6m 40s'},
  {id:'david', name:'David Brown', title:'Support Agent', initials:'DB', color:'#0EA5E9', tickets:11, csat:4.6, sla:93, resolved:178, avgHandle:'8m 05s'},
  {id:'alex', name:'Alex Thomas', title:'Support Agent', initials:'AT', color:'#9333EA', tickets:9, csat:4.4, sla:88, resolved:150, avgHandle:'9m 12s'},
];

const CUSTOMERS = {
  'john': {id:'john', name:'John Smith', email:'john.smith@gmail.com', phone:'+1 415 555 0148', plan:'Pro Plan', since:'Mar 2023', location:'Austin, TX', tickets:6, csat:4.7},
  'sarah': {id:'sarah', name:'Sarah Johnson', email:'sarah.j@outlook.com', phone:'+1 312 555 0199', plan:'Business Plan', since:'Jul 2022', location:'Chicago, IL', tickets:9, csat:4.3},
  'rahul': {id:'rahul', name:'Rahul Sharma', email:'rahul.sharma@yahoo.in', phone:'+91 98765 43210', plan:'Pro Plan', since:'Jan 2024', location:'Bengaluru, IN', tickets:4, csat:4.9},
  'priya': {id:'priya', name:'Priya Patel', email:'priya.patel@gmail.com', phone:'+91 90123 45678', plan:'Starter Plan', since:'Sep 2024', location:'Ahmedabad, IN', tickets:3, csat:3.8},
};

const CH_ICON = {Email:'mail','Website Chat':'chat',WhatsApp:'whatsapp',Instagram:'instagram',Facebook:'facebook'};
const CH_COLOR = {Email:'#0369A1','Website Chat':'#4F46E5',WhatsApp:'#15803D',Instagram:'#C026D3',Facebook:'#1D4ED8'};const TICKETS = [
  {
    id: 'TCK-10234',
    customer: 'sarah',
    subject: 'Need invoice with updated company GST number',
    category: 'Billing',
    channel: 'Email',
    status: 'Resolved',
    priority: 'Low',
    agent: 'ai',
    sla: 'Closed on time',
    slaState: 'done',
    created: 'Mon, 9:30 AM',
    updated: '2 days ago',
    sentiment: '🙂 Happy',
    confidence: '98%',
    summary: 'Sarah needed invoice updated with company GST number. AI Assistant matched the request, automatically updated the profile field, re-generated the PDF invoice, and provided the download link. Customer confirmed resolution. Resolved.',
    messages: [
      { role: 'customer', text: 'Hi, I need my invoice for last month updated to show our corporate tax ID: GSTIN-9920188A. Can you re-issue?', timestamp: 'Mon, 9:30 AM' },
      { role: 'ai', text: 'Searching Help Center... I found article "Updating Tax and Invoice Details". You can update your tax registration details under Billing Settings. I\'ve also automatically updated your account details to GSTIN-9920188A and re-generated your last invoice. You can download it here: <a href="#" class="link" onclick="alert(\'Invoice INV-9021 downloaded!\')">invoice_INV-9021.pdf</a>. Did that resolve your issue?', timestamp: 'Mon, 9:31 AM' },
      { role: 'customer', text: 'Yes, perfect! That was so fast, thank you!', timestamp: 'Mon, 9:35 AM' },
      { role: 'ai', text: 'Glad I could help! I\'ve marked this ticket as resolved. Have a great day!', timestamp: 'Mon, 9:35 AM' }
    ],
    history: [
      { time: 'Mon, 9:30 AM', text: 'Ticket created via Email' },
      { time: '1 min later', text: 'AI matched tax request, updated profile & generated invoice PDF' },
      { time: '5 min later', text: 'Customer confirmed resolution, ticket closed automatically' }
    ],
    suggestedReplies: [
      "The updated invoice has been sent. Let me know if you need any past invoices updated."
    ],
    notes: 'Automatically resolved by AI Agent. Stripe metadata synchronized. — AI Assistant, 2 days ago'
  },
  {
    id: 'TCK-10235',
    customer: 'sarah',
    subject: 'Two-factor login code never arrives',
    category: 'Technical',
    channel: 'Website Chat',
    status: 'Resolved',
    priority: 'High',
    agent: 'alex',
    sla: 'Closed on time',
    slaState: 'done',
    created: 'Today, 7:55 AM',
    updated: '25 min ago',
    sentiment: '🙂 Happy',
    confidence: '55%',
    summary: 'Sarah is blocked because SMS 2FA codes are not arriving. AI suggested troubleshooting steps but customer requested human agent. Handoff via Chat triggered. Alex Thomas connected, identified carrier spam filter block in Auth0 logs, and sent a bypass link. Resolved.',
    messages: [
      { role: 'customer', text: 'I\'ve been trying to log in for the last hour but the SMS verification code never arrives on my phone. I\'m locked out.', timestamp: 'Today, 7:55 AM' },
      { role: 'ai', text: 'Searching Help Center... SMS delivery failures can be caused by carrier blocks or service latency. If you are locked out, I can connect you to an agent.<div style="margin-top:10px; border-top:1px solid var(--border); padding-top:10px;"><div style="font-weight:700; margin-bottom:8px; font-size:12.5px;">Would you like to connect with our support executors?</div><div style="display:flex; gap:8px;"><button class="btn btn-primary btn-sm" style="font-size:11px; padding:4px 8px;" disabled>💬 Chat with Agent</button><button class="btn btn-sm" style="font-size:11px; padding:4px 8px; background:var(--surface); border:1px solid var(--border);" disabled>📞 Call Support</button></div></div>', timestamp: 'Today, 7:56 AM' },
      { role: 'customer', text: '💬 Connect via Chat', timestamp: 'Today, 7:57 AM' },
      { role: 'ai', text: 'Let me connect you with our support team...', timestamp: 'Today, 7:57 AM' },
      { role: 'agent', text: '<span style="color:var(--success); font-weight:700;">● Alex Thomas (Technical Support) has joined the chat.</span>', timestamp: 'Today, 7:58 AM' },
      { role: 'agent', text: 'Hi Sarah! I see you are locked out due to 2FA verification issues. I am reviewing our Auth0 carrier logs right now.', timestamp: 'Today, 7:59 AM' },
      { role: 'customer', text: 'Yes please, I really need to access my files.', timestamp: 'Today, 8:00 AM' },
      { role: 'agent', text: 'I found the log: the carrier blocked the code as spam. I\'ve sent a temporary bypass link to your backup email. Let me know if that works.', timestamp: 'Today, 8:02 AM' },
      { role: 'customer', text: 'Got it! I am logged in now. Thank you so much!', timestamp: 'Today, 8:03 AM' },
      { role: 'agent', text: 'Fantastic! I\'ll mark this as resolved. Have a great day!', timestamp: 'Today, 8:04 AM' }
    ],
    history: [
      { time: 'Today, 7:55 AM', text: 'Ticket created via Website Chat' },
      { time: '1 min later', text: 'AI suggested troubleshooting steps and offered handoff options' },
      { time: '2 min later', text: 'Customer selected Chat option' },
      { time: '3 min later', text: 'Alex Thomas accepted the chat' },
      { time: '7 min later', text: 'Bypass link sent to backup email' },
      { time: '9 min later', text: 'Customer confirmed successful login. Resolved.' }
    ],
    suggestedReplies: [
      "Hi Sarah, glad everything is working now. I will close this ticket.",
      "Let us know if you experience SMS delivery latency in the future."
    ],
    notes: 'Checking Auth0 logs for SMS API errors. Bypass link worked. — Alex, 25 min ago'
  },
  {
    id: 'TCK-10236',
    customer: 'john',
    subject: 'Downgrade plan before next billing cycle',
    category: 'Billing',
    channel: 'Facebook',
    status: 'Open',
    priority: 'Medium',
    agent: 'emma',
    sla: '2h 45m left',
    slaState: 'ok',
    created: 'Today, 9:48 AM',
    updated: '8 min ago',
    sentiment: '🙂 Happy',
    confidence: '80%',
    summary: 'John wants to downgrade from Pro to Starter. AI explained downgrade rules, prompted handoff options. Customer chose to connect via Call and was routed to the phone line. Emma Wilson picked up the voice call and is finalizing the plan downgrade.',
    messages: [
      { role: 'customer', text: 'I want to downgrade my account to the Starter plan before the next invoice charges on Nov 15th. Will I lose my project data?', timestamp: 'Today, 9:48 AM' },
      { role: 'ai', text: 'Searching Help Center... Downgrading takes effect at the end of the billing cycle. Your data will be kept but extra features will be locked. Would you like me to guide you?<div style="margin-top:10px; border-top:1px solid var(--border); padding-top:10px;"><div style="font-weight:700; margin-bottom:8px; font-size:12.5px;">Would you like to connect with our support executors?</div><div style="display:flex; gap:8px;"><button class="btn btn-primary btn-sm" style="font-size:11px; padding:4px 8px;" disabled>💬 Chat with Agent</button><button class="btn btn-sm" style="font-size:11px; padding:4px 8px; background:var(--surface); border:1px solid var(--border);" disabled>📞 Call Support</button></div></div>', timestamp: 'Today, 9:49 AM' },
      { role: 'customer', text: '📞 Connect via Call', timestamp: 'Today, 9:50 AM' },
      { role: 'ai', text: 'Sure! Please call our support line at <b style="color:var(--primary); font-size:14px;">+1 (800) 555-0199</b> (Toll-Free). Our executors are available 24/7 to assist you.', timestamp: 'Today, 9:51 AM' },
      { role: 'agent', text: '● Emma Wilson took inbound voice call. Customer verified. Manually scheduled plan downgrade to Starter. Project retention limits confirmed. Saved.', timestamp: 'Today, 9:58 AM' },
      { role: 'customer', text: 'Thank you for the verification on the phone!', timestamp: 'Today, 9:59 AM' }
    ],
    history: [
      { time: 'Today, 9:48 AM', text: 'Ticket created via Facebook Messenger' },
      { time: '1 min later', text: 'AI explained data retention rules, offered walkthrough and handoff options' },
      { time: '2 min later', text: 'Customer selected Call Support option' },
      { time: '3 min later', text: 'Customer redirected to phone support line' },
      { time: '10 min later', text: 'Emma Wilson completed call and manually updated subscription' }
    ],
    suggestedReplies: [
      "Hi John, I\'ve verified your account. Your Starter limit allows up to 3 projects, so your 2 active projects will remain safe."
    ],
    notes: 'Redirected to inbound phone queue. Awaiting phone dispatch logs. — Emma'
  },
  {
    id: 'TCK-10237',
    customer: 'sarah',
    subject: 'App crashes when I upload a profile photo',
    category: 'Technical',
    channel: 'Email',
    status: 'New',
    priority: 'Medium',
    agent: null,
    sla: '4h 00m left',
    slaState: 'ok',
    created: 'Today, 8:40 AM',
    updated: '40 min ago',
    sentiment: '😟 Frustrated',
    confidence: '48%',
    summary: 'Sarah is experiencing app crashes when uploading profile images. AI tried suggesting clearing browser cache and converting to JPEG, but the issue persists. Customer chose to connect via chat, but all agents are busy. Ticket escalated to queue.',
    messages: [
      { role: 'customer', text: 'Whenever I try to upload my profile photo, the entire page freezes and the app crashes. Please help, I need this for my business profile.', timestamp: 'Today, 8:40 AM' },
      { role: 'ai', text: 'Searching Help Center... I found article "Troubleshooting profile uploads". Please make sure your image is under 5MB and is in PNG or JPEG format. Try clearing your browser cache.<div style="margin-top:10px; border-top:1px solid var(--border); padding-top:10px;"><div style="font-weight:700; margin-bottom:8px; font-size:12.5px;">Would you like to connect with our support executors?</div><div style="display:flex; gap:8px;"><button class="btn btn-primary btn-sm" style="font-size:11px; padding:4px 8px;" disabled>💬 Chat with Agent</button><button class="btn btn-sm" style="font-size:11px; padding:4px 8px; background:var(--surface); border:1px solid var(--border);" disabled>📞 Call Support</button></div></div>', timestamp: 'Today, 8:41 AM' },
      { role: 'customer', text: '💬 Connect via Chat', timestamp: 'Today, 8:42 AM' },
      { role: 'ai', text: 'Let me connect you with our support team...', timestamp: 'Today, 8:42 AM' },
      { role: 'ai', text: 'All support agents are currently busy assisting other customers. An executor will reach out to you shortly.', timestamp: 'Today, 8:43 AM' }
    ],
    history: [
      { time: 'Today, 8:40 AM', text: 'Ticket created via Email' },
      { time: '1 min later', text: 'AI suggested article & offered support handoff options' },
      { time: '2 min later', text: 'Customer selected Chat option' },
      { time: '3 min later', text: 'Agents busy, escalated to support queue' }
    ],
    suggestedReplies: [
      "Hi Sarah, sorry for the hassle. Could you share the original image file so our dev team can reproduce the crash?",
      "I\'ve escalated this to our Tier 2 technical engineering team. We\'ll inspect our upload service logs for your account."
    ],
    notes: ''
  },
  {
    id: 'TCK-10238',
    customer: 'rahul',
    subject: 'Order #88213 still shows "Processing"',
    category: 'Orders',
    channel: 'WhatsApp',
    status: 'Waiting',
    priority: 'Medium',
    agent: 'david',
    sla: '1h 05m left',
    slaState: 'warn',
    created: 'Yesterday, 6:02 PM',
    updated: '2 hr ago',
    sentiment: '😐 Neutral',
    confidence: '72%',
    summary: 'Rahul is asking about order #88213 which has been stuck in "Processing" for 3 days. AI matched the order number but found shipment delay due to stock check. Escalated to David. Warehouse has been contacted.',
    messages: [
      { role: 'customer', text: 'My order #88213 was placed three days ago but it still shows "Processing" status. When will it ship?', timestamp: 'Yesterday, 6:02 PM' },
      { role: 'ai', text: 'Searching Help Center... I found your order #88213. Typically orders ship in 24-48 hours. Let me check the courier queue.', timestamp: 'Yesterday, 6:04 PM' },
      { role: 'ai', text: 'It seems there\'s an inventory delay for the Pro Hub item. Connecting you to a support agent to coordinate shipping updates.', timestamp: 'Yesterday, 6:05 PM' },
      { role: 'agent', text: 'Hi Rahul! I have contacted the warehouse manager to expedite your Pro Hub shipment. I am waiting for their confirmation and will update you shortly.', timestamp: 'Yesterday, 6:15 PM' }
    ],
    history: [
      { time: 'Yesterday, 6:02 PM', text: 'Ticket created via WhatsApp' },
      { time: '2 min later', text: 'AI scanned order status database' },
      { time: '3 min later', text: 'AI detected courier/stock delay, auto-transferred to agent queue' }
    ],
    suggestedReplies: [
      "Hi Rahul, apologies for the wait. The Pro Hub was briefly backordered but is back in stock. It will ship today.",
      "I\'ve verified with the warehouse — your order is scheduled for priority dispatch this afternoon."
    ],
    notes: 'Warehouse team confirms shipment will go out by 4 PM today. — David, 2 hr ago'
  },
  {
    id: 'TCK-10239',
    customer: 'priya',
    subject: 'Refund not received after 10 business days',
    category: 'Refund',
    channel: 'Instagram',
    status: 'Escalated',
    priority: 'Urgent',
    agent: 'alex',
    sla: 'Overdue by 38m',
    slaState: 'bad',
    created: 'Yesterday, 2:15 PM',
    updated: '5 min ago',
    sentiment: '😡 Angry',
    confidence: '35%',
    summary: 'Priya is angry that her refund has not arrived after 10 days. AI checked billing logs but could not trace the bank transaction reference. Transferred to Alex Thomas.',
    messages: [
      { role: 'customer', text: 'You told me the refund would take 5-7 days. It has been 10 business days now and still nothing in my account! This is unacceptable.', timestamp: 'Yesterday, 2:15 PM' },
      { role: 'ai', text: 'Searching Help Center... Refunds usually take 5-7 business days but bank processing may add 2-3 days. Let me search our billing logs for transaction reference RF-88231.', timestamp: 'Yesterday, 2:16 PM' },
      { role: 'customer', text: 'I already checked with my bank, they see no pending transactions. Stop giving me auto-responses and put me through to a real person immediately!', timestamp: 'Yesterday, 2:18 PM' },
      { role: 'ai', text: 'I understand your frustration. I am escalating this to our billing supervisor right now.', timestamp: 'Yesterday, 2:19 PM' },
      { role: 'agent', text: 'Hi Priya, I sincerely apologize for the delay. I am manually tracking this with our billing lead to get you the Stripe transaction reference ID.', timestamp: 'Yesterday, 2:25 PM' }
    ],
    history: [
      { time: 'Yesterday, 2:15 PM', text: 'Ticket created via Instagram DM' },
      { time: '1 min later', text: 'AI searched Help Center & billing records' },
      { time: '3 min later', text: 'Customer requested immediate human agent escalation' },
      { time: '4 min later', text: 'Escalated to Billing Supervisor (Alex Thomas) as URGENT' }
    ],
    suggestedReplies: [
      "Hi Priya, I sincerely apologize for the delay. I am manually tracking this with our Stripe manager right now.",
      "I\'ve retrieved the bank transaction reference ID: Stripe ch_3N2x... Please share this ID with your bank\'s supervisor."
    ],
    notes: 'Triggered manual review on Stripe dashboard. Processing reference check. — Alex, 5 min ago'
  }
];

const KB_ARTICLES = [
  {id:'kb1', title:'How to reset your account password', cat:'Account', views:'12.4k', helpful:96, updated:'2 weeks ago', body:"If you're locked out of your account, go to the login page and select 'Forgot password'. Enter the email linked to your account and we'll send a secure reset link valid for 30 minutes. After resetting, you'll be signed out of all other devices for your security."},
  {id:'kb2', title:'Understanding your monthly invoice', cat:'Billing', views:'9.8k', helpful:92, updated:'4 days ago', body:"Your monthly invoice includes your base subscription fee, any add-ons, prorated charges for mid-cycle upgrades, and applicable taxes. Invoices are generated on your billing date and emailed automatically, and are also available anytime under Billing > Invoices."},
  {id:'kb3', title:'Tracking your order shipment', cat:'Orders', views:'15.1k', helpful:94, updated:'1 week ago', body:"Once your order ships, you'll receive a tracking number by email and SMS. You can also track any order from My Orders > Order Details. Delivery estimates are shown per courier and update automatically as the package moves."},
  {id:'kb4', title:'Refund policy and processing timelines', cat:'Refunds', views:'11.2k', helpful:89, updated:'3 days ago', body:"Approved refunds are processed within 5-7 business days to your original payment method. Bank processing can add another 2-3 days depending on your provider. You'll get an email confirmation the moment your refund is issued."},
  {id:'kb5', title:'Updating your payment method', cat:'Billing', views:'7.5k', helpful:91, updated:'5 days ago', body:"Go to Billing > Payment Methods to add a new card or remove an old one. Your next invoice will automatically charge the default method. Updating your card does not affect your current billing cycle dates."},
  {id:'kb6', title:'Troubleshooting login issues', cat:'Account', views:'13.9k', helpful:95, updated:'6 days ago', body:"Most login issues are caused by expired sessions or cached credentials. Try clearing your browser cache, confirming caps-lock is off, and checking for a pending password-reset email. If two-factor codes aren't arriving, check your phone's signal and spam folder."},
];

const CHANNELS = [
  {name:'Email', icon:'mail', status:'Connected', detail:'support@brand.com', volume:'482 / week'},
  {name:'Website Chat', icon:'chat', status:'Connected', detail:'brand.com widget', volume:'610 / week'},
  {name:'WhatsApp', icon:'whatsapp', status:'Connected', detail:'+1 415 555 0100', volume:'295 / week'},
  {name:'Instagram', icon:'instagram', status:'Connected', detail:'@brand.official', volume:'140 / week'},
  {name:'Facebook', icon:'facebook', status:'Needs attention', detail:'/brand.page', volume:'88 / week'},
];

const NOTIFS = [
  {icon:'alert', text:'SLA breach risk on TCK-10237 (Priya Patel)', time:'2 min ago', color:'var(--danger)'},
  {icon:'ticket', text:'New ticket TCK-10241 assigned to queue', time:'6 min ago', color:'var(--primary)'},
  {icon:'smile', text:'John Smith rated TCK-10238 5 stars', time:'25 min ago', color:'var(--success)'},
  {icon:'bot', text:'AI resolved 14 tickets automatically today', time:'1 hr ago', color:'#9333EA'},
];

/* ---------------- App State ---------------- */
const STATE = {
  role: 'landing',      // landing | customer | agent | manager | admin
  view: null,
  params: {},
  activeChannelFilter: 'All',
};

function setRole(role){
  STATE.role = role;
  STATE.view = DEFAULT_VIEW[role];
  STATE.params = {};
  render();
}
function navigate(view, params={}){
  STATE.view = view;
  STATE.params = params;
  render();
  const c = document.querySelector('.content');
  if(c) c.scrollTop = 0;
}
const DEFAULT_VIEW = {customer:'live-chat', agent:'agent-dashboard', manager:'manager-dashboard', admin:'admin-dashboard'};

/* ---------------- Navigation config per role ---------------- */
const NAV = {
  customer: [
    {section:'Support', items:[
      {id:'live-chat', label:'Live Chat', icon:'chat'},
      {id:'profile', label:'Customer Profile', icon:'user'},
    ]},
  ],
  agent: [
    {section:'Workspace', items:[
      {id:'agent-dashboard', label:'Dashboard', icon:'home'},
      {id:'unified-inbox', label:'All Messages', icon:'inbox'},
      {id:'ticket-queue', label:'Ticket Queue', icon:'list'},
      {id:'macros', label:'Quick Replies', icon:'sparkle'},
      {id:'kb-search', label:'Help Center', icon:'book'},
    ]},
  ],
  manager: [
    {section:'Insights', items:[
      {id:'manager-dashboard', label:'Dashboard', icon:'home'},
      {id:'analytics', label:'Analytics', icon:'chart'},
      {id:'agent-performance', label:'Agent Performance', icon:'users'},
      {id:'sla-dashboard', label:'SLA Dashboard', icon:'clock'},
      {id:'ticket-reports', label:'Ticket Reports', icon:'ticket'},
      {id:'workflow-automation', label:'Workflow Automation', icon:'refresh'},
    ]},
  ],
  admin: [
    {section:'Administration', items:[
      {id:'admin-dashboard', label:'Dashboard', icon:'home'},
      {id:'user-management', label:'User Management', icon:'users'},
      {id:'channel-integrations', label:'Channel Integrations', icon:'plug'},
      {id:'kb-management', label:'Help Center Mgmt', icon:'book'},
      {id:'ai-settings', label:'AI Settings', icon:'bot'},
      {id:'roles-permissions', label:'Roles & Permissions', icon:'shield'},
      {id:'system-settings', label:'System Settings', icon:'gear'},
    ]},
  ],
};

const ROLE_LABEL = {customer:'Customer', agent:'Support Agent', manager:'Support Manager', admin:'Administrator'};
const ROLE_USER = {
  customer:{name:'John Smith', initials:'JS'},
  agent:{name:'Emma Wilson', initials:'EW'},
  manager:{name:'Olivia Reyes', initials:'OR'},
  admin:{name:'Marcus Lee', initials:'ML'},
};
const TITLES = {
  'customer-portal':'Home', 'my-tickets':'My Tickets', 'live-chat':'Live Chat', 'ai-chatbot':'AI Assistant',
  'knowledge-base':'Help Center', 'ticket-details':'Ticket Details', 'profile':'My Profile',
  'agent-dashboard':'Agent Dashboard', 'unified-inbox':'All Messages', 'ticket-queue':'Ticket Queue',
  'customer-profile':'Customer Profile', 'macros':'Quick Replies', 'kb-search':'Help Center',
  'manager-dashboard':'Manager Dashboard', 'analytics':'Analytics', 'agent-performance':'Agent Performance',
  'sla-dashboard':'SLA Dashboard', 'ticket-reports':'Ticket Reports', 'workflow-automation':'Workflow Automation',
  'admin-dashboard':'Admin Dashboard', 'user-management':'User Management', 'channel-integrations':'Channel Integrations',
  'kb-management':'Help Center Management', 'ai-settings':'AI Settings', 'roles-permissions':'Roles & Permissions',
  'system-settings':'System Settings', 'kb-article':'Article',
};

/* ---------------- Root render ---------------- */
function render(){
  const app = document.getElementById('app');
  if(STATE.role === 'landing'){ app.innerHTML = renderLanding(); attachLandingEvents(); return; }
  app.innerHTML = renderShell();
  attachGlobalEvents();
}

function attachGlobalEvents(){
  const sel = document.getElementById('roleSelect');
  if(sel) sel.addEventListener('change', e=>setRole(e.target.value));
}

function renderShell(){
  const role = STATE.role;
  const nav = NAV[role];
  const user = ROLE_USER[role];
  const title = TITLES[STATE.view] || 'Dashboard';
  return `
  <div class="sidebar">
    <div class="sidebar-brand">
      <div class="brand-mark">S</div>
      <div>
        <div class="brand-name">SupportHub</div>
        <div class="brand-sub">AI Omnichannel Platform</div>
      </div>
    </div>
    <div class="role-switcher">
      <div class="role-switcher-label">Demo — Viewing as</div>
      <select id="roleSelect">
        <option value="customer" ${role==='customer'?'selected':''}>Customer</option>
        <option value="agent" ${role==='agent'?'selected':''}>Support Agent</option>
        <option value="manager" ${role==='manager'?'selected':''}>Support Manager</option>
        <option value="admin" ${role==='admin'?'selected':''}>Admin</option>
      </select>
    </div>
    <div class="nav-scroll">
      ${nav.map(sec=>`
        <div class="nav-section-label">${sec.section}</div>
        ${sec.items.map(it=>`
          <a class="nav-item ${STATE.view===it.id?'active':''}" onclick="navigate('${it.id}')">
            ${icon(it.icon)}<span>${it.label}</span>
          </a>`).join('')}
      `).join('')}
    </div>
    <div class="sidebar-foot">
      <div class="user-chip">
        <div class="avatar">${user.initials}</div>
        <div>
          <div class="name">${user.name}</div>
          <div class="role">${ROLE_LABEL[role]}</div>
        </div>
        <a class="icon-btn" style="margin-left:auto;border:none;" onclick="setRole('landing')" title="Switch role">${icon('logout',16)}</a>
      </div>
    </div>
  </div>
  <div class="main">
    <div class="topbar">
      <div class="topbar-left">
        <div class="page-title">${title}</div>
      </div>
      <div class="topbar-right">
        <div class="searchbox">${icon('search',16)}<span>Search tickets, customers, articles…</span></div>
        <div class="icon-btn" title="Notifications" onclick="alert('4 new notifications — see the bell for the demo list.')">
          ${icon('bell',18)}<span class="badge-dot">4</span>
        </div>
        <div class="avatar" style="width:34px;height:34px;font-size:12px;">${user.initials}</div>
      </div>
    </div>
    <div class="content">
      ${renderView()}
    </div>
  </div>`;
}

function renderView(){
  try{
    const fn = VIEWS[STATE.view];
    if(fn) return fn(STATE.params);
    return VIEWS[DEFAULT_VIEW[STATE.role]]();
  }catch(e){
    console.error(e);
    return `<div class="empty-state">${icon('alert',40)}<div>Something went wrong rendering this screen.</div></div>`;
  }
}

/* ---------------- Landing / role picker ---------------- */
function renderLanding(){
  const roles = [
    {id:'customer', icon:'user', title:'Customer', desc:'Browse the customer portal, chat with the AI assistant, track tickets and search the help center.'},
    {id:'agent', icon:'inbox', title:'Support Agent', desc:'Work all messages, reply with AI-suggested responses, and resolve tickets across channels.'},
    {id:'manager', icon:'chart', title:'Support Manager', desc:'Monitor SLA compliance, AI resolution rate, agent performance and automation workflows.'},
    {id:'admin', icon:'gear', title:'Admin', desc:'Manage users, channel integrations, help center content, AI settings and permissions.'},
  ];
  return `
  <div style="width:100%; min-height:100vh; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:40px 20px; background:radial-gradient(circle at 20% 15%, #EEF0FE 0%, #F6F7FC 45%), var(--bg);">
    <div style="max-width:900px; width:100%; text-align:center; margin-bottom:36px;">
      <div style="display:inline-flex; align-items:center; gap:10px; margin-bottom:18px;">
        <div class="brand-mark" style="width:44px;height:44px;font-size:19px;">S</div>
        <div style="font-family:var(--font-display); font-weight:800; font-size:22px;">SupportHub</div>
      </div>
      <h1 style="font-size:34px; margin:0 0 10px 0;">AI-Powered Omnichannel Customer Support</h1>
      <p style="font-size:15px; color:var(--text-muted); max-width:600px; margin:0 auto;">A clickable product prototype for demos and client presentations. Choose a role below to explore that workspace — every screen is connected and uses realistic sample data.</p>
    </div>
    <div class="grid grid-4" style="max-width:1040px; width:100%;">
      ${roles.map(r=>`
        <div class="card" style="cursor:pointer; text-align:left;" onclick="setRole('${r.id}')">
          <div class="ai-glow-icon" style="width:40px;height:40px;border-radius:10px; margin-bottom:14px;">${icon(r.icon,20)}</div>
          <div style="font-family:var(--font-display); font-weight:800; font-size:16px; margin-bottom:6px;">${r.title}</div>
          <div style="font-size:12.5px; color:var(--text-muted); line-height:1.5; margin-bottom:14px;">${r.desc}</div>
          <div style="font-size:12.5px; font-weight:700; color:var(--primary); display:flex; align-items:center; gap:4px;">Enter workspace ${icon('chev',14)}</div>
        </div>
      `).join('')}
    </div>
    <div style="margin-top:28px;" class="chip">${icon('sparkle',14)} Prototype only — no real backend, AI or data is connected</div>
  </div>`;
}
function attachLandingEvents(){}

/* ---------------- Shared helpers ---------------- */
function statusPill(status){
  const map = {New:'new', Open:'open', Waiting:'waiting', Escalated:'escalated', Resolved:'resolved', Closed:'closed'};
  const cls = map[status] || 'open';
  return `<span class="pill pill-${cls}"><span class="pill-dot" style="background:currentColor;"></span>${status}</span>`;
}
function priorityColor(p){
  return {Urgent:'var(--danger)', High:'#C2410C', Medium:'var(--warning)', Low:'var(--text-faint)'}[p] || 'var(--text-faint)';
}
function slaColor(state){
  return {ok:'var(--success)', warn:'var(--warning)', bad:'var(--danger)', done:'var(--text-faint)'}[state];
}
function chanIcon(ch, size=14){
  return `<span style="color:${CH_COLOR[ch]}; display:inline-flex;">${icon(CH_ICON[ch], size)}</span>`;
}
function agentById(id){ 
  if (id === 'ai') return { id: 'ai', name: 'AI Assistant', initials: '🤖', color: '#9333EA', title: 'AI Bot' };
  return AGENTS.find(a=>a.id===id); 
}
function custById(id){ return CUSTOMERS[id]; }
function fmtAgent(id){
  if(!id) return `<span style="color:var(--text-faint);">Unassigned</span>`;
  const a = agentById(id);
  if (id === 'ai') return `<span style="display:inline-flex; align-items:center; gap:6px;"><span class="avatar-sm" style="background:${a.color}; font-size:10px; display:flex; align-items:center; justify-content:center;">${a.initials}</span>${a.name}</span>`;
  return `<span style="display:inline-flex; align-items:center; gap:6px;"><span class="avatar-sm" style="background:${a.color};">${a.initials}</span>${a.name}</span>`;
}
function ticketRow(t, onClickView='ticket-details'){
  const c = custById(t.customer);
  return `
  <tr class="tbl-row" onclick="navigate('${onClickView}',{id:'${t.id}'})">
    <td><span class="mono">${t.id}</span></td>
    <td>
      <div style="font-weight:700;">${t.subject}</div>
      <div style="font-size:11.5px; color:var(--text-faint); margin-top:2px;">${c.name} · ${t.category}</div>
    </td>
    <td>${chanIcon(t.channel)} <span style="font-size:12px;">${t.channel}</span></td>
    <td>${statusPill(t.status)}</td>
    <td><span style="color:${priorityColor(t.priority)}; font-weight:700; font-size:12px;">${t.priority}</span></td>
    <td>${fmtAgent(t.agent)}</td>
    <td><span style="color:${slaColor(t.slaState)}; font-weight:700; font-size:12px;">${t.sla}</span></td>
  </tr>`;
}
function ticketTable(tickets, onClickView){
  return `
  <table>
    <thead><tr><th>Ticket</th><th>Subject</th><th>Channel</th><th>Status</th><th>Priority</th><th>Agent</th><th>SLA</th></tr></thead>
    <tbody>${tickets.map(t=>ticketRow(t,onClickView)).join('')}</tbody>
  </table>`;
}
function kpi(icon_, label, value, delta, deltaUp, color){
  return `
  <div class="kpi-card">
    <div class="kpi-top">
      <div class="kpi-icon" style="background:${color}1A; color:${color};">${icon(icon_,17)}</div>
      ${delta?`<span class="kpi-delta ${deltaUp?'up':'down'}">${icon(deltaUp?'arrowUp':'arrowDown',12)}${delta}</span>`:''}
    </div>
    <div class="kpi-value">${value}</div>
    <div class="kpi-label">${label}</div>
  </div>`;
}

/* ============================================================
   CUSTOMER VIEWS
   ============================================================ */
function v_customerPortal(){
  const my = TICKETS.filter(t=>t.customer==='john');
  return `
  <div class="section-title">Welcome back, John 👋</div>
  <div class="section-sub">Here's what's happening with your account today.</div>

  <div class="ai-box" style="margin-bottom:20px;">
    <div class="ai-box-inner" style="display:flex; align-items:center; gap:16px;">
      <div class="ai-glow-icon" style="width:44px;height:44px;border-radius:12px;">${icon('bot',22)}</div>
      <div style="flex:1;">
        <div class="ai-tag">${icon('sparkle',12)} AI Assistant</div>
        <div style="font-weight:700; font-size:14.5px; margin:3px 0 2px 0;">Have a question? Get an instant answer.</div>
        <div style="font-size:12.5px; color:var(--text-muted);">Our AI searches the help center instantly and can create a ticket if you still need a human.</div>
      </div>
      <button class="btn btn-ai" onclick="navigate('ai-chatbot')">${icon('send',14)} Ask now</button>
    </div>
  </div>

  <div class="grid grid-4" style="margin-bottom:22px;">
    ${kpi('ticket','Open Tickets', my.filter(t=>!['Resolved','Closed'].includes(t.status)).length, null,true,'#4F46E5')}
    ${kpi('check','Resolved This Month','5', '+2', true, '#15803D')}
    ${kpi('clock','Avg. Response Time','18 min', '-4 min', true, '#0369A1')}
    ${kpi('smile','My Avg. CSAT', '4.7 / 5', null, true, '#9333EA')}
  </div>

  <div class="grid grid-3">
    <div class="card" style="cursor:pointer;" onclick="navigate('my-tickets')">
      <div class="ai-glow-icon" style="background:var(--primary); width:36px;height:36px;border-radius:9px; margin-bottom:12px;">${icon('ticket',18)}</div>
      <div style="font-weight:700; margin-bottom:4px;">My Tickets</div>
      <div style="font-size:12.5px; color:var(--text-muted);">Track the status of every request you've submitted.</div>
    </div>
    <div class="card" style="cursor:pointer;" onclick="navigate('live-chat')">
      <div class="ai-glow-icon" style="background:#0EA5E9; width:36px;height:36px;border-radius:9px; margin-bottom:12px;">${icon('chat',18)}</div>
      <div style="font-weight:700; margin-bottom:4px;">Live Chat</div>
      <div style="font-size:12.5px; color:var(--text-muted);">Chat in real time with our support team.</div>
    </div>
    <div class="card" style="cursor:pointer;" onclick="navigate('knowledge-base')">
      <div class="ai-glow-icon" style="background:#9333EA; width:36px;height:36px;border-radius:9px; margin-bottom:12px;">${icon('book',18)}</div>
      <div style="font-weight:700; margin-bottom:4px;">Help Center</div>
      <div style="font-size:12.5px; color:var(--text-muted);">Browse help articles and step-by-step guides.</div>
    </div>
  </div>

  <div class="card" style="margin-top:20px;">
    <div class="card-title">Recent tickets <a class="btn btn-ghost btn-sm" onclick="navigate('my-tickets')">View all ${icon('chev',13)}</a></div>
    ${ticketTable(my.slice(0,4))}
  </div>`;
}

function v_myTickets(){
  const my = TICKETS.filter(t=>t.customer==='john');
  return `
  <div class="section-title">My Tickets</div>
  <div class="section-sub">All the requests you've submitted, across every channel.</div>
  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
    <div class="tabs" style="margin-bottom:0; border-bottom:none;">
      <div class="tab active">All (${my.length})</div>
      <div class="tab">Open (${my.filter(t=>!['Resolved','Closed'].includes(t.status)).length})</div>
      <div class="tab">Closed (${my.filter(t=>['Resolved','Closed'].includes(t.status)).length})</div>
    </div>
    <button class="btn btn-primary" onclick="navigate('ai-chatbot')">${icon('plus',14)} New Request</button>
  </div>
  <div class="card" style="padding:0;">
    ${ticketTable(my)}
  </div>`;
}

function v_ticketDetailsCustomer(t, c){
  const messagesList = t.messages || [
    { role: 'customer', text: t.subject, timestamp: t.created }
  ];
  const assignedAgentName = t.agent ? (AGENTS.find(a => a.id === t.agent)?.name || 'Support Agent') : 'AI Assistant';

  return `
  <div class="breadcrumb"><a onclick="navigate('my-tickets')">My Tickets</a> / ${t.id}</div>
  <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:18px;">
    <div>
      <div class="section-title" style="margin-bottom:4px;">${t.subject}</div>
      <div style="display:flex; gap:10px; align-items:center;">${statusPill(t.status)}<span class="mono">${t.id}</span><span class="chip">${chanIcon(t.channel)} ${t.channel}</span></div>
    </div>
  </div>
  <div class="grid" style="grid-template-columns:2fr 1fr; align-items:start;">
    <div class="card">
      <div class="card-title">Conversation</div>
      <div class="conversation-container" style="display:flex; flex-direction:column; gap:14px; max-height:380px; overflow-y:auto; padding:8px 0;">
        ${messagesList.map(m => {
          if (m.role === 'customer') {
            return `<div class="msg out" style="align-self:flex-end; max-width:85%;">${m.text}<div class="msg-meta" style="color:#E0E0FF;">You · ${m.timestamp}</div></div>`;
          } else if (m.role === 'ai') {
            return `<div class="ai-box" style="align-self:flex-start; max-width:85%;"><div class="ai-box-inner" style="padding:10px 12px;"><div class="ai-tag">${icon('sparkle',10)} AI Assistant</div><div style="font-size:12.5px; margin-top:4px;">${m.text}</div></div></div>`;
          } else {
            const agentObj = AGENTS.find(a => a.id === t.agent) || { name: 'Support Agent', title: 'Agent' };
            return `<div class="msg in" style="max-width:85%;">${m.text}<div class="msg-meta">${agentObj.name} · ${agentObj.title} · ${m.timestamp}</div></div>`;
          }
        }).join('')}
      </div>
      <div class="chat-input-bar" style="margin-top:16px; border-top:1px solid var(--border); padding-top:14px;">
        <input id="customer-reply-input" placeholder="Reply to ${assignedAgentName}…" onkeydown="if(event.key==='Enter') sendCustomerReply('${t.id}')"/>
        <button class="icon-btn">${icon('paperclip',16)}</button>
        <button class="btn btn-primary btn-sm" onclick="sendCustomerReply('${t.id}')">${icon('send',14)} Send</button>
      </div>
    </div>
    <div style="display:flex; flex-direction:column; gap:16px;">
      <div class="card">
        <div class="card-title">Ticket Info</div>
        <div style="display:flex; flex-direction:column; gap:10px; font-size:12.5px;">
          <div style="display:flex; justify-content:space-between;"><span style="color:var(--text-faint);">Category</span><b>${t.category}</b></div>
          <div style="display:flex; justify-content:space-between;"><span style="color:var(--text-faint);">Priority</span><b style="color:${priorityColor(t.priority)};">${t.priority}</b></div>
          <div style="display:flex; justify-content:space-between;"><span style="color:var(--text-faint);">Assigned agent</span>${fmtAgent(t.agent)}</div>
          <div style="display:flex; justify-content:space-between;"><span style="color:var(--text-faint);">Created</span><b>${t.created}</b></div>
        </div>
      </div>
      <div class="card">
        <div class="card-title">Need something else?</div>
        <button class="btn" style="width:100%; justify-content:center; margin-bottom:8px;" onclick="navigate('knowledge-base')">${icon('book',14)} Browse Help Articles</button>
        <button class="btn" style="width:100%; justify-content:center;" onclick="navigate('live-chat')">${icon('chat',14)} Start Live Chat</button>
      </div>
    </div>
  </div>`;
}

/* ---------- Live Chat Stateful State and Simulation ---------- */
const CUSTOMER_CHATS = [
  {
    id: 'chat-1',
    title: 'Double Charge Refund',
    status: 'Completed',
    agentName: 'Emma Wilson',
    agentInitials: 'EW',
    agentColor: '#4F46E5',
    ticket: 'TCK-10234',
    msgs: [
      { sender: 'agent', text: 'Hi John! Thanks for reaching out on live chat, how can I help today?', time: '10:01 AM' },
      { sender: 'user', text: 'Hey Emma, following up on my duplicate charge ticket TCK-10234.', time: '10:02 AM' },
      { sender: 'agent', text: 'I can see it — refund of $29.00 is already processing, should land in 5-7 business days. Anything else?', time: '10:03 AM' },
      { sender: 'user', text: 'That\'s perfect, thank you!', time: '10:03 AM' },
      { sender: 'agent', text: 'Happy to help 😊 Have a great day!', time: '10:04 AM' }
    ]
  },
  {
    id: 'chat-2',
    title: 'Replacement Request',
    status: 'Completed',
    agentName: 'Emma Wilson',
    agentInitials: 'EW',
    agentColor: '#4F46E5',
    ticket: 'TCK-10238',
    msgs: [
      { sender: 'user', text: 'Hi, I received the wrong item for order #88213.', time: 'Mon, 11:00 AM' },
      { sender: 'agent', text: 'Oh, sorry about that! Let create a replacement order for you.', time: 'Mon, 11:05 AM' },
      { sender: 'agent', text: 'Replacement order #88215 has been created. You can keep or recycle the wrong item.', time: 'Mon, 11:08 AM' },
      { sender: 'user', text: 'Awesome, thanks!', time: 'Mon, 11:10 AM' }
    ]
  },
  {
    id: 'chat-3',
    title: 'Plan Downgrade Query',
    status: 'Active',
    agentName: 'Emma Wilson',
    agentInitials: 'EW',
    agentColor: '#4F46E5',
    ticket: 'TCK-10242',
    msgs: [
      { sender: 'user', text: 'Hey, I want to downgrade my plan before the next billing cycle.', time: 'Today, 9:48 AM' },
      { sender: 'agent', text: 'I can help you with that. We can set it to downgrade to the Starter plan starting next month.', time: 'Today, 9:50 AM' },
      { sender: 'user', text: 'Perfect, let\'s do that.', time: 'Today, 9:52 AM' }
    ]
  }
];

let activeChatId = 'chat-3';

window.startNewChat = function() {
  const newId = 'chat-' + (CUSTOMER_CHATS.length + 1);
  const newChat = {
    id: newId,
    title: 'New Chat Session',
    status: 'Active',
    agentName: 'AI Support Bot',
    agentInitials: 'AI',
    agentColor: 'var(--ai-grad)',
    ticket: 'Draft',
    msgs: [
      { sender: 'agent', text: 'Hello! I am your AI Assistant. How can I help you today?', time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }
    ]
  };
  CUSTOMER_CHATS.push(newChat);
  activeChatId = newId;
  render();
  setTimeout(scrollToBottom, 50);
};

window.sendCustomerMessage = function() {
  const input = document.getElementById('chatInput');
  if (!input) return;
  const text = input.value.trim();
  if (!text) return;
  
  const chat = CUSTOMER_CHATS.find(c => c.id === activeChatId);
  if (!chat) return;

  const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  chat.msgs.push({ sender: 'user', text: text, time: timeStr });
  input.value = '';
  
  render();
  scrollToBottom();
  
  if (chat.agentConnected) {
    setTimeout(() => {
      chat.msgs.push({
        sender: 'agent',
        text: "I've checked the details for you. Let me go ahead and resolve this right away. Is there anything else you'd like me to look into?",
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      });
      render();
      scrollToBottom();
    }, 1000);
    return;
  }
  
  // Simulate reply after 1s
  setTimeout(() => {
    let replyText = "";
    let showHandoffOptions = false;
    
    const lowerText = text.toLowerCase();
    if (lowerText.includes('hello') || lowerText.includes('hi') || lowerText.includes('hey')) {
      replyText = "Hello! Hope you are having a wonderful day. How can I assist you?";
    } else if (lowerText.includes('thank')) {
      replyText = "You're very welcome! Let me know if there's anything else I can do for you.";
    } else if (lowerText.includes('human') || lowerText.includes('agent') || lowerText.includes('executor') || lowerText.includes('support') || lowerText.includes('call') || lowerText.includes('chat')) {
      replyText = "I understand you'd like to speak with a human support executor.";
      showHandoffOptions = true;
    } else {
      if (lowerText.includes('billing') || lowerText.includes('charge') || lowerText.includes('money') || lowerText.includes('refund')) {
        replyText = "I found 3 articles matching 'billing'. You can manage subscriptions directly under Settings > Billing.";
      } else if (lowerText.includes('order') || lowerText.includes('shipping') || lowerText.includes('delivery')) {
        replyText = "Standard delivery takes 3-5 business days. You can track your shipments using the link sent in your invoice email.";
      } else {
        replyText = "I searched our Help Center but couldn't find a direct answer to your query.";
      }
      showHandoffOptions = true;
    }
    
    if (showHandoffOptions) {
      replyText += `
        <div style="margin-top:10px; border-top:1px solid var(--border); padding-top:10px;">
          <div style="font-weight:700; margin-bottom:8px; font-size:12.5px; color:var(--text-muted);">Would you like to connect with our support executors?</div>
          <div style="display:flex; gap:8px;">
            <button class="btn btn-primary btn-sm" onclick="selectHandoffOption('${chat.id}', 'chat')" style="font-size:11.5px; padding:6px 10px;">💬 Chat with Agent</button>
            <button class="btn btn-sm" onclick="selectHandoffOption('${chat.id}', 'call')" style="font-size:11.5px; padding:6px 10px; background:var(--surface); border:1px solid var(--border);">📞 Call Support</button>
          </div>
        </div>
      `;
    }
    
    chat.msgs.push({
      sender: 'agent',
      text: replyText,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    });
    
    render();
    scrollToBottom();
  }, 1000);
};

window.selectHandoffOption = function(chatId, option) {
  const chat = CUSTOMER_CHATS.find(c => c.id === chatId);
  if (!chat) return;
  
  const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  
  if (option === 'chat') {
    chat.msgs.push({ sender: 'user', text: '💬 Connect via Chat', time: timeStr });
    render();
    scrollToBottom();
    
    setTimeout(() => {
      chat.msgs.push({
        sender: 'agent',
        text: 'Let me connect you with our support team...',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      });
      render();
      scrollToBottom();
      
      const isBusy = Math.random() > 0.5;
      
      setTimeout(() => {
        if (isBusy) {
          chat.msgs.push({
            sender: 'agent',
            text: 'All support agents are currently busy assisting other customers. An executor will reach out to you shortly.',
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          });
          render();
          scrollToBottom();
        } else {
          chat.agentConnected = true;
          chat.msgs.push({
            sender: 'agent',
            text: '<span style="color:var(--success); font-weight:700;">● Emma Wilson (Support Lead) has joined the chat.</span>',
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          });
          render();
          scrollToBottom();
          
          setTimeout(() => {
            chat.msgs.push({
              sender: 'agent',
              text: 'Hello! I am Emma Wilson from technical support. I\'ve reviewed your conversation history. How can I assist you with this today?',
              time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            });
            render();
            scrollToBottom();
          }, 1000);
        }
      }, 1500);
      
    }, 1000);
    
  } else if (option === 'call') {
    chat.msgs.push({ sender: 'user', text: '📞 Connect via Call', time: timeStr });
    render();
    scrollToBottom();
    
    setTimeout(() => {
      chat.msgs.push({
        sender: 'agent',
        text: 'Sure! Please call our support line at <b style="color:var(--primary); font-size:14px;">+1 (800) 555-0199</b> (Toll-Free). Our executors are available 24/7 to assist you.',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      });
      render();
      scrollToBottom();
    }, 1000);
  }
};

window.scrollToBottom = function() {
  const msgsDivs = document.querySelectorAll('.chat-msgs');
  msgsDivs.forEach(div => {
    div.scrollTop = div.scrollHeight;
  });
};

function v_liveChat(){
  const activeChat = CUSTOMER_CHATS.find(c => c.id === activeChatId) || CUSTOMER_CHATS[0];
  
  return `
  <div class="section-title">Live Chat</div>
  <div class="section-sub">You're connected with our support team in real time.</div>
  <div class="card" style="padding:0; height:560px; display:flex; overflow:hidden;">
    <!-- Sidebar: Chat History -->
    <div class="chat-sidebar">
      <button class="new-chat-btn" onclick="startNewChat()">
        ${icon('plus',14)} New Chat
      </button>
      <div style="font-size:11px; text-transform:uppercase; letter-spacing:.05em; color:var(--text-faint); font-weight:700; margin-top:8px;">
        Chat History
      </div>
      <div class="chat-history-list">
        ${CUSTOMER_CHATS.map(c => {
          const isActive = c.id === activeChatId;
          const statusClass = c.status === 'Active' ? 'chat-status-active' : 'chat-status-completed';
          const rawLastMsg = c.msgs.length > 0 ? c.msgs[c.msgs.length - 1].text : 'No messages';
          const lastMsg = rawLastMsg.split('<')[0].replace(/<[^>]*>/g, '').replace(/\s+/g, ' ').trim();
          const lastMsgTime = c.msgs.length > 0 ? c.msgs[c.msgs.length - 1].time : '';
          return `
          <div class="chat-history-item ${isActive ? 'active' : ''}" onclick="activeChatId='${c.id}'; render(); setTimeout(scrollToBottom, 50);">
            <div class="chat-history-item-top">
              <div class="chat-history-title">${c.title}</div>
              <span class="chat-status-badge ${statusClass}">${c.status}</span>
            </div>
            <div class="chat-history-preview" title="${lastMsg}">${lastMsg}</div>
            <div class="chat-history-meta">
              <span>Linked: ${c.ticket}</span>
              <span>${lastMsgTime}</span>
            </div>
          </div>`;
        }).reverse().join('')}
      </div>
    </div>
    
    <!-- Main Chat Window -->
    <div class="chat-window" style="flex:1;">
      <!-- Chat Header -->
      <div style="padding:14px 18px; border-bottom:1px solid var(--border); display:flex; align-items:center; justify-content:space-between; background:var(--surface);">
        <div style="display:flex; align-items:center; gap:10px;">
          <span class="avatar-sm" style="background:${activeChat.agentColor}; width:34px;height:34px;">${activeChat.agentInitials}</span>
          <div>
            <div style="font-weight:700; font-size:13.5px;">${activeChat.agentName}</div>
            <div style="font-size:11px; color:var(--success); display:flex; align-items:center; gap:4px;">
              <span style="width:6px;height:6px;border-radius:50%;background:var(--success);display:inline-block;"></span>
              Online
            </div>
          </div>
        </div>
        <div style="text-align:right;">
          <div style="font-size:11px; color:var(--text-faint); font-weight:700; text-transform:uppercase; letter-spacing:.05em;">Linked Ticket</div>
          <div class="chip" style="margin-top:4px; font-size:11.5px; cursor:pointer;" onclick="navigate('ticket-details',{id:'${activeChat.ticket}'})">
            ${icon('ticket',12)} ${activeChat.ticket}
          </div>
        </div>
      </div>
      
      <!-- Chat Messages -->
      <div class="chat-msgs">
        ${activeChat.msgs.map(m => {
          const isUser = m.sender === 'user';
          const msgClass = isUser ? 'out' : 'in';
          const senderName = isUser ? 'You' : activeChat.agentName;
          return `
          <div class="msg ${msgClass}">
            ${m.text}
            <div class="msg-meta" style="${isUser ? 'color:#E0E0FF;' : ''}">${senderName} · ${m.time}</div>
          </div>`;
        }).join('')}
      </div>
      
      <!-- Chat Input -->
      <div class="chat-input-bar">
        <input id="chatInput" placeholder="Type a message…" onkeydown="if(event.key === 'Enter') sendCustomerMessage()"/>
        <button class="icon-btn" onclick="alert('File attachment is not simulated in this demo.')">${icon('paperclip',16)}</button>
        <button class="btn btn-primary btn-sm" onclick="sendCustomerMessage()">${icon('send',14)} Send</button>
      </div>
    </div>
  </div>`;
}

const CHATBOT_SCRIPT = [
  {role:'user', text:"My order hasn't arrived yet, order #88213"},
  {role:'ai', text:"Let me look that up for you.", searching:true},
  {role:'ai', text:"I found your order #88213 — it shipped Nov 4th and is currently in transit with FedEx, estimated delivery is tomorrow by 8 PM. Would you like the live tracking link?"},
  {role:'user', text:"Yes please"},
  {role:'ai', text:"Here you go: track.fedex-demo.com/88213. I've also linked our 'Tracking your order shipment' article below in case it's delayed further. Did that answer your question?"},
];
function v_aiChatbot(){
  return `
  <div class="section-title">AI Assistant</div>
  <div class="section-sub">Ask anything — I'll search the help center instantly and loop in a human if needed.</div>
  <div class="grid" style="grid-template-columns:2fr 1fr; align-items:start;">
    <div class="card" style="padding:0; height:560px; display:flex; flex-direction:column;">
      <div style="padding:14px 18px; border-bottom:1px solid var(--border); display:flex; align-items:center; gap:10px;">
        <div class="ai-glow-icon" style="width:32px;height:32px;border-radius:8px;">${icon('bot',16)}</div>
        <div>
          <div style="font-weight:700; font-size:13.5px;">SupportHub AI</div>
          <div style="font-size:11px; color:var(--text-faint);">Trained on your help center · Answers instantly</div>
        </div>
      </div>
      <div class="chat-msgs">
        ${CHATBOT_SCRIPT.map(m=>{
          if(m.role==='user') return `<div class="msg out">${m.text}</div>`;
          if(m.searching) return `<div class="ai-box" style="align-self:flex-start; max-width:75%;"><div class="ai-box-inner"><div class="ai-tag">${icon('search',11)} Searching Help Center…</div></div></div>`;
          if(m.role==='agent') return `<div class="msg in" style="align-self:flex-start; background:var(--surface-alt); border-bottom-left-radius:4px; max-width:68%;">${m.text}<div class="msg-meta">Emma Wilson (Support Lead)</div></div>`;
          return `<div class="ai-box" style="align-self:flex-start; max-width:80%;"><div class="ai-box-inner"><div class="ai-tag">${icon('sparkle',11)} AI Assistant</div><div style="font-size:13.5px; margin-top:5px;">${m.text}</div></div></div>`;
        }).join('')}
        ${CHATBOT_SCRIPT.length === 5 ? `
        <div style="align-self:flex-start; display:flex; gap:8px; margin-top: 4px;">
          <button class="btn btn-sm" onclick="navigate('kb-article',{id:'kb3'})">${icon('book',13)} View Article</button>
          <button class="btn btn-sm" onclick="alert('Marked resolved — thanks for confirming!')">${icon('check',13)} Yes, resolved</button>
          <button class="btn btn-sm btn-primary" onclick="navigate('ticket-details',{id:'TCK-10238'})">${icon('user',13)} Talk to a human</button>
        </div>
        ` : ''}
      </div>
      <div class="chat-input-bar">
        <input id="chatbotInput" placeholder="Ask a question…" onkeydown="if(event.key === 'Enter') sendChatbotMessage()"/>
        <button class="btn btn-ai btn-sm" onclick="sendChatbotMessage()">${icon('send',14)} Ask AI</button>
      </div>
    </div>
    <div style="display:flex; flex-direction:column; gap:16px;">
      <div class="card">
        <div class="card-title">How it works</div>
        <div class="timeline">
          <div class="timeline-item"><div class="timeline-time">Step 1</div><div class="timeline-text">You ask a question in plain language</div></div>
          <div class="timeline-item"><div class="timeline-time">Step 2</div><div class="timeline-text">AI searches the Help Center for a match</div></div>
          <div class="timeline-item"><div class="timeline-time">Step 3</div><div class="timeline-text">AI replies instantly, or escalates to an agent</div></div>
          <div class="timeline-item" style="padding-bottom:0;"><div class="timeline-time">Step 4</div><div class="timeline-text">Issue resolved, or a ticket is created automatically</div></div>
        </div>
      </div>
      <div class="card" style="cursor:pointer;" onclick="navigate('knowledge-base')">
        <div class="card-title">Related articles</div>
        <div style="font-size:12.5px; font-weight:700; color:var(--primary);">Tracking your order shipment →</div>
      </div>
    </div>
  </div>`;
}

window.sendChatbotMessage = function() {
  const input = document.getElementById('chatbotInput');
  if (!input) return;
  const text = input.value.trim();
  if (!text) return;
  
  CHATBOT_SCRIPT.push({ role: 'user', text: text });
  input.value = '';
  render();
  scrollToBottom();
  
  if (STATE.chatbotAgentConnected) {
    setTimeout(() => {
      CHATBOT_SCRIPT.push({
        role: 'agent',
        text: "I've checked the details for you. Let me go ahead and resolve this right away. Is there anything else you'd like me to look into?"
      });
      render();
      scrollToBottom();
    }, 1000);
    return;
  }
  
  // Show searching spinner
  CHATBOT_SCRIPT.push({ role: 'ai', text: 'Searching Help Center...', searching: true });
  render();
  scrollToBottom();
  
  setTimeout(() => {
    // Remove the searching item
    const idx = CHATBOT_SCRIPT.findIndex(x => x.searching);
    if (idx !== -1) {
      CHATBOT_SCRIPT.splice(idx, 1);
    }
    
    let replyText = "";
    let showHandoffOptions = false;
    const lowerText = text.toLowerCase();
    
    if (lowerText.includes('hello') || lowerText.includes('hi') || lowerText.includes('hey')) {
      replyText = "Hello! I am SupportHub AI. How can I assist you with our products today?";
    } else if (lowerText.includes('thank')) {
      replyText = "You're very welcome! Let know if you need anything else.";
    } else if (lowerText.includes('human') || lowerText.includes('agent') || lowerText.includes('executor') || lowerText.includes('support') || lowerText.includes('call') || lowerText.includes('chat')) {
      replyText = "I understand you'd like to reach a support executor.";
      showHandoffOptions = true;
    } else {
      if (lowerText.includes('billing') || lowerText.includes('charge') || lowerText.includes('money') || lowerText.includes('refund')) {
        replyText = "Billing adjustments usually take 5-7 business days. To check transaction status, please connect with a billing specialist.";
      } else if (lowerText.includes('order') || lowerText.includes('shipping') || lowerText.includes('delivery')) {
        replyText = "We ship orders globally. Standard shipping timelines are 3-5 days. Let me know if you need shipment tracking assistance.";
      } else {
        replyText = "I searched our documentation database but couldn't find a solution for this issue.";
      }
      showHandoffOptions = true;
    }
    
    if (showHandoffOptions) {
      replyText += `
        <div style="margin-top:10px; border-top:1px solid var(--border); padding-top:10px;">
          <div style="font-weight:700; margin-bottom:8px; font-size:12.5px; color:var(--text-muted);">Would you like to connect with our support executors?</div>
          <div style="display:flex; gap:8px;">
            <button class="btn btn-primary btn-sm" onclick="selectChatbotHandoff('chat')" style="font-size:11.5px; padding:6px 10px;">💬 Chat with Agent</button>
            <button class="btn btn-sm" onclick="selectChatbotHandoff('call')" style="font-size:11.5px; padding:6px 10px; background:var(--surface); border:1px solid var(--border);">📞 Call Support</button>
          </div>
        </div>
      `;
    }
    
    CHATBOT_SCRIPT.push({ role: 'ai', text: replyText });
    render();
    scrollToBottom();
  }, 1200);
};

window.selectChatbotHandoff = function(option) {
  if (option === 'chat') {
    CHATBOT_SCRIPT.push({ role: 'user', text: '💬 Connect via Chat' });
    render();
    scrollToBottom();
    
    setTimeout(() => {
      CHATBOT_SCRIPT.push({ role: 'ai', text: 'Let me connect you with our support team...' });
      render();
      scrollToBottom();
      
      const isBusy = Math.random() > 0.5;
      
      setTimeout(() => {
        if (isBusy) {
          CHATBOT_SCRIPT.push({ role: 'ai', text: 'All support agents are currently busy assisting other customers. An executor will reach out to you shortly.' });
          render();
          scrollToBottom();
        } else {
          STATE.chatbotAgentConnected = true;
          CHATBOT_SCRIPT.push({ role: 'agent', text: '<span style="color:var(--success); font-weight:700;">● Emma Wilson (Support Lead) has joined the chat.</span>' });
          render();
          scrollToBottom();
          
          setTimeout(() => {
            CHATBOT_SCRIPT.push({ role: 'agent', text: "Hello! I am Emma Wilson from technical support. I've reviewed your conversation history. How can I assist you with this today?" });
            render();
            scrollToBottom();
          }, 1000);
        }
      }, 1500);
    }, 1000);
    
  } else if (option === 'call') {
    CHATBOT_SCRIPT.push({ role: 'user', text: '📞 Connect via Call' });
    render();
    scrollToBottom();
    
    setTimeout(() => {
      CHATBOT_SCRIPT.push({ role: 'ai', text: 'Sure! Please call our support line at <b style="color:var(--primary); font-size:14px;">+1 (800) 555-0199</b> (Toll-Free). Our executors are available 24/7 to assist you.' });
      render();
      scrollToBottom();
    }, 1000);
  }
};

function v_knowledgeBase(){
  return `
  <div class="section-title">Help Center</div>
  <div class="section-sub">Find answers instantly, or ask the AI Assistant.</div>
  <div class="searchbox" style="width:100%; max-width:none; margin-bottom:22px; padding:13px 16px;">${icon('search',17)}<span>Search articles — e.g. "refund", "password", "invoice"…</span></div>
  <div class="grid grid-4" style="margin-bottom:24px;">
    ${['Account','Billing','Orders','Refunds'].map((c,i)=>`
      <div class="card" style="text-align:center; cursor:pointer;" onclick="navigate('knowledge-base')">
        <div class="ai-glow-icon" style="margin:0 auto 10px auto; background:${['#4F46E5','#0EA5E9','#9333EA','#DB2777'][i]}; width:38px;height:38px;border-radius:10px;">${icon(['user','ticket','globe','refresh'][i],18)}</div>
        <div style="font-weight:700; font-size:13.5px;">${c}</div>
        <div style="font-size:11.5px; color:var(--text-faint); margin-top:2px;">${KB_ARTICLES.filter(a=>a.cat===c || (c==='Refunds'&&a.cat==='Refunds')).length || 2} articles</div>
      </div>
    `).join('')}
  </div>
  <div class="card-title" style="font-size:16px;">Popular articles</div>
  <div class="grid grid-2">
    ${KB_ARTICLES.map(a=>`
      <div class="card" style="cursor:pointer;" onclick="navigate('kb-article',{id:'${a.id}'})">
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
          <div style="font-weight:700; font-size:14px; margin-bottom:6px; max-width:85%;">${a.title}</div>
          <span class="chip" style="flex-shrink:0;">${a.cat}</span>
        </div>
        <div style="font-size:12px; color:var(--text-faint);">${a.views} views · ${a.helpful}% found helpful · updated ${a.updated}</div>
      </div>
    `).join('')}
  </div>`;
}

function v_kbArticle(p){
  const a = KB_ARTICLES.find(x=>x.id===p.id) || KB_ARTICLES[0];
  return `
  <div class="breadcrumb"><a onclick="navigate('knowledge-base')">Help Center</a> / ${a.cat}</div>
  <div class="grid" style="grid-template-columns:2.2fr 1fr; align-items:start;">
    <div class="card">
      <span class="chip">${a.cat}</span>
      <h1 style="font-size:23px; margin:12px 0 6px 0;">${a.title}</h1>
      <div style="font-size:12px; color:var(--text-faint); margin-bottom:18px;">Updated ${a.updated} · ${a.views} views</div>
      <p style="font-size:14px; line-height:1.75; color:#333148;">${a.body}</p>
      <div style="margin-top:24px; padding-top:18px; border-top:1px solid var(--border); display:flex; align-items:center; justify-content:space-between;">
        <div style="font-size:13px; font-weight:700;">Was this article helpful?</div>
        <div style="display:flex; gap:8px;">
          <button class="btn btn-sm">👍 Yes</button>
          <button class="btn btn-sm">👎 No</button>
        </div>
      </div>
    </div>
    <div style="display:flex; flex-direction:column; gap:16px;">
      <div class="card">
        <div class="card-title">Still need help?</div>
        <button class="btn btn-ai" style="width:100%; justify-content:center; margin-bottom:8px;" onclick="navigate('ai-chatbot')">${icon('bot',14)} Ask AI Assistant</button>
        <button class="btn" style="width:100%; justify-content:center;" onclick="navigate('live-chat')">${icon('chat',14)} Start Live Chat</button>
      </div>
    </div>
  </div>`;
}

function v_profile(){
  const c = CUSTOMERS.john;
  return `
  <div class="section-title">My Profile</div>
  <div class="section-sub">Manage your account details and preferences.</div>
  <div class="grid" style="grid-template-columns:1fr 2fr; align-items:start;">
    <div class="card" style="text-align:center;">
      <div class="avatar" style="width:64px;height:64px; font-size:22px; margin:0 auto 12px auto;">JS</div>
      <div style="font-weight:800; font-size:16px;">${c.name}</div>
      <div style="font-size:12.5px; color:var(--text-faint); margin-bottom:10px;">${c.plan} · Member since ${c.since}</div>
      <button class="btn" style="width:100%; justify-content:center;">Edit Photo</button>
    </div>
    <div class="card">
      <div class="card-title">Account Details</div>
      <div class="grid grid-2">
        <div><div class="settings-sub">Full name</div><div style="font-weight:700; font-size:13.5px;">${c.name}</div></div>
        <div><div class="settings-sub">Email</div><div style="font-weight:700; font-size:13.5px;">${c.email}</div></div>
        <div><div class="settings-sub">Phone</div><div style="font-weight:700; font-size:13.5px;">${c.phone}</div></div>
        <div><div class="settings-sub">Location</div><div style="font-weight:700; font-size:13.5px;">${c.location}</div></div>
      </div>
      <div style="margin-top:18px;">
        <div class="settings-row"><div><div class="settings-label">Email notifications</div><div class="settings-sub">Ticket updates and replies</div></div><div class="switch on"></div></div>
        <div class="settings-row"><div><div class="settings-label">WhatsApp notifications</div><div class="settings-sub">Quick updates via WhatsApp</div></div><div class="switch on"></div></div>
        <div class="settings-row"><div><div class="settings-label">Marketing emails</div><div class="settings-sub">Product news and tips</div></div><div class="switch"></div></div>
      </div>
    </div>
  </div>`;
}

/* ============================================================
   SUPPORT AGENT VIEWS
   ============================================================ */
function v_agentDashboard(){
  const mine = TICKETS.filter(t=>t.agent==='emma');
  return `
  <div class="section-title">Good morning, Emma</div>
  <div class="section-sub">You have ${mine.filter(t=>!['Resolved','Closed'].includes(t.status)).length} active tickets today.</div>
  <div class="grid grid-4" style="margin-bottom:20px;">
    ${kpi('inbox','Open Tickets','24','+3',true,'#4F46E5')}
    ${kpi('ticket','Assigned to Me', mine.length.toString(), null,true,'#0EA5E9')}
    ${kpi('clock','Waiting Customers','7','-2',true,'#B45309')}
    ${kpi('alert','SLA Alerts','3','+1',false,'#DC2626')}
  </div>
  <div class="grid" style="grid-template-columns:2fr 1fr; align-items:start; margin-bottom:20px;">
    <div class="card">
      <div class="card-title">My Queue <a class="btn btn-ghost btn-sm" onclick="navigate('unified-inbox')">Open inbox ${icon('chev',13)}</a></div>
      ${ticketTable(mine)}
    </div>
    <div class="card">
      <div class="card-title">My CSAT Score</div>
      <div style="text-align:center; padding:10px 0;">
        <div style="font-family:var(--font-display); font-size:40px; font-weight:800; color:var(--success);">4.8</div>
        <div class="stars">★★★★★</div>
        <div style="font-size:12px; color:var(--text-faint); margin-top:6px;">Based on 212 resolved tickets</div>
      </div>
      <div style="margin-top:10px;">
        <div class="stat-bar-row"><div class="stat-bar-label">5 stars</div><div class="stat-bar-track"><div class="stat-bar-fill" style="width:78%; background:var(--success);"></div></div><div class="stat-bar-val">78%</div></div>
        <div class="stat-bar-row"><div class="stat-bar-label">4 stars</div><div class="stat-bar-track"><div class="stat-bar-fill" style="width:15%; background:#4ADE80;"></div></div><div class="stat-bar-val">15%</div></div>
        <div class="stat-bar-row"><div class="stat-bar-label">≤3 stars</div><div class="stat-bar-track"><div class="stat-bar-fill" style="width:7%; background:var(--warning);"></div></div><div class="stat-bar-val">7%</div></div>
      </div>
    </div>
  </div>
  <div class="ai-box">
    <div class="ai-box-inner" style="display:flex; align-items:center; gap:16px;">
      <div class="ai-glow-icon" style="width:40px;height:40px;border-radius:11px;">${icon('sparkle',20)}</div>
      <div style="flex:1;">
        <div class="ai-tag">${icon('bot',12)} AI Insight</div>
        <div style="font-weight:700; font-size:13.5px; margin:3px 0 2px 0;">14 tickets were fully resolved by AI today without human input.</div>
        <div style="font-size:12px; color:var(--text-muted);">That's 31% of total volume — up 6% from last week.</div>
      </div>
      <button class="btn" onclick="navigate('unified-inbox')">View Inbox</button>
    </div>
  </div>`;
}

function v_unifiedInbox(){
  const channels = ['All', 'Email', 'Website Chat', 'WhatsApp', 'Instagram', 'Facebook'];
  const filtered = STATE.activeChannelFilter === 'All'
    ? TICKETS
    : TICKETS.filter(t => t.channel === STATE.activeChannelFilter);
    
  return `
  <div class="section-title">All Messages</div>
  <div class="section-sub">All customer conversations, across every channel, in one place.</div>
  <div style="display:flex; gap:10px; margin-bottom:14px; flex-wrap:wrap;">
    ${channels.map(c => {
      const active = STATE.activeChannelFilter === c;
      const style = active
        ? `background:var(--primary-light); border-color:#DEE0FB; color:var(--primary-dark); font-weight:700; cursor:pointer;`
        : `cursor:pointer;`;
      const label = c === 'All' ? 'All Channels' : c;
      const iconPrefix = c === 'All' ? '' : `${chanIcon(c,13)} `;
      return `<span class="chip" style="${style}" onclick="STATE.activeChannelFilter='${c}'; render();">${iconPrefix}${label}</span>`;
    }).join('')}
    <button class="btn btn-sm" style="margin-left:auto;">${icon('filter',13)} Filter</button>
  </div>
  <div class="card" style="padding:0;">
    ${ticketTable(filtered)}
  </div>`;
}

function v_ticketQueue(){
  const cols = ['New','Open','Waiting','Escalated','Resolved'];
  const colColor = {New:'var(--info)',Open:'var(--primary)',Waiting:'var(--warning)',Escalated:'var(--danger)',Resolved:'var(--success)'};
  return `
  <div class="section-title">Ticket Queue</div>
  <div class="section-sub">Drag-and-drop kanban view of all tickets by status.</div>
  <div class="kanban">
    ${cols.map(status=>{
      const items = TICKETS.filter(t=>t.status===status);
      return `
      <div class="kanban-col">
        <div class="kanban-col-head"><span style="display:flex; align-items:center; gap:6px;"><span style="width:8px;height:8px;border-radius:50%; background:${colColor[status]}; display:inline-block;"></span>${status}</span><span class="chip" style="padding:2px 8px;">${items.length}</span></div>
        ${items.map(t=>`
          <div class="kanban-card" onclick="navigate('ticket-details',{id:'${t.id}'})">
            <div class="tck-id">${t.id} · ${chanIcon(t.channel,11)} ${t.channel}</div>
            <div class="tck-subj">${t.subject}</div>
            <div style="display:flex; align-items:center; justify-content:space-between;">
              <span style="font-size:11px; color:${priorityColor(t.priority)}; font-weight:700;">${t.priority}</span>
              ${t.agent?`<span class="avatar-sm" style="background:${agentById(t.agent).color}; width:22px;height:22px; font-size:9.5px;">${agentById(t.agent).initials}</span>`:`<span style="font-size:10.5px; color:var(--text-faint);">Unassigned</span>`}
            </div>
          </div>`).join('') || `<div style="font-size:12px; color:var(--text-faint); text-align:center; padding:20px 0;">No tickets</div>`}
      </div>`;
    }).join('')}
  </div>`;
}

function v_ticketDetailsAgent(t,c){
  const summaryText = t.summary || `No AI summary generated for ${t.id}.`;
  const sentimentText = t.sentiment || '😐 Neutral';
  const confidenceText = t.confidence || 'N/A';
  const notesText = t.notes || '';
  
  const historyList = t.history || [
    { time: 'Today', text: 'Ticket created' }
  ];
  
  const suggestedReplies = t.suggestedReplies || [
    "I'll look into this for you right away.",
    "Let me check our systems and get back to you."
  ];

  const messagesList = t.messages || [
    { role: 'customer', text: t.subject, timestamp: t.created }
  ];

  const assigneeDropdown = `
    <select id="ticket-assignee-select" onchange="assignTicket('${t.id}', this.value)" style="width:100%; border:1px solid var(--border); border-radius:9px; padding:8px 12px; font-size:13px; background:var(--surface); color:var(--text); font-family:inherit; cursor:pointer;">
      <option value="" ${!t.agent ? 'selected' : ''}>Unassigned</option>
      ${AGENTS.map(a => `<option value="${a.id}" ${t.agent === a.id ? 'selected' : ''}>${a.name} (${a.title})</option>`).join('')}
    </select>
  `;

  return `
  <div class="breadcrumb"><a onclick="navigate('unified-inbox')">All Messages</a> / ${t.id}</div>
  <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:16px;">
    <div>
      <div class="section-title" style="margin-bottom:4px;">${t.subject}</div>
      <div style="display:flex; gap:10px; align-items:center;">${statusPill(t.status)}<span class="mono">${t.id}</span><span class="chip">${chanIcon(t.channel)} ${t.channel}</span><span style="font-size:12px; color:${priorityColor(t.priority)}; font-weight:700;">${t.priority} priority</span></div>
    </div>
    <div style="display:flex; gap:8px;">
      <button class="btn btn-primary btn-sm" onclick="alert('Ticket ${t.id} marked as Resolved. Customer will be asked for CSAT feedback.')">${icon('check',13)} Resolve</button>
    </div>
  </div>

  <div class="grid" style="grid-template-columns:2.1fr 1fr; align-items:start;">
    <div style="display:flex; flex-direction:column; gap:16px;">
      <div class="ai-box">
        <div class="ai-box-inner">
          <div class="ai-tag">${icon('sparkle',11)} AI Summary</div>
          <div style="font-size:13px; margin-top:6px; line-height:1.6;">${summaryText}</div>
          <div style="display:flex; gap:10px; margin-top:10px;">
            <span class="chip">Sentiment: ${sentimentText}</span>
            <span class="chip">Confidence: ${confidenceText}</span>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-title">Conversation</div>
        <div class="conversation-container" style="display:flex; flex-direction:column; gap:14px; max-height:380px; overflow-y:auto; padding:8px 0;">
          ${messagesList.map(m => {
            if (m.role === 'customer') {
              return `<div class="msg in" style="max-width:85%;">${m.text}<div class="msg-meta">${c.name} · ${m.timestamp}</div></div>`;
            } else if (m.role === 'ai') {
              return `<div class="ai-box" style="max-width:85%; margin-bottom: 4px;"><div class="ai-box-inner" style="padding:10px 12px;"><div class="ai-tag">${icon('sparkle',10)} AI Assistant (to customer)</div><div style="font-size:12.5px; margin-top:4px;">${m.text}</div></div></div>`;
            } else {
              return `<div class="msg out" style="max-width:85%; align-self:flex-end;">${m.text}<div class="msg-meta" style="color:#E0E0FF;">You · ${m.timestamp}</div></div>`;
            }
          }).join('')}
        </div>
      </div>

      <div class="ai-box">
        <div class="ai-box-inner">
          <div class="ai-tag">${icon('sparkle',11)} AI Suggested Replies</div>
          <div style="display:flex; flex-direction:column; gap:8px; margin-top:10px;">
            ${suggestedReplies.map(reply => `
              <div style="background:var(--surface); border:1px solid var(--border); border-radius:9px; padding:10px 12px; font-size:12.5px; display:flex; justify-content:space-between; align-items:center; gap:10px;">
                <span>"${reply}"</span>
                <button class="btn btn-sm" onclick="useSuggestedReply(this)" style="flex-shrink:0;">Use</button>
              </div>
            `).join('')}
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-title">Reply</div>
        <textarea id="reply-textarea" placeholder="Type your reply…" style="width:100%; min-height:80px; border:1px solid var(--border); border-radius:9px; padding:10px 12px; font-family:inherit; font-size:13px; resize:vertical;"></textarea>
        <div style="display:flex; justify-content:space-between; margin-top:10px;">
          <div style="display:flex; gap:8px;">
            <button class="btn btn-sm">${icon('paperclip',13)} Attach</button>
            <button class="btn btn-sm" onclick="navigate('macros')">${icon('sparkle',13)} Quick Replies</button>
          </div>
          <button class="btn btn-primary btn-sm" onclick="sendAgentReply('${t.id}')">${icon('send',13)} Send Reply</button>
        </div>
      </div>

      <div class="card">
        <div class="card-title">Internal Notes <span class="chip">Not visible to customer</span></div>
        ${notesText ? `<div style="background:var(--warning-bg); border-radius:9px; padding:10px 12px; font-size:12.5px; margin-bottom:10px;">${notesText}</div>` : ''}
        <div style="display:flex; gap:8px;">
          <input id="note-input" placeholder="Add an internal note…" style="flex:1; border:1px solid var(--border); border-radius:9px; padding:9px 12px; font-size:12.5px; font-family:inherit;" onkeydown="if(event.key==='Enter') addInternalNote('${t.id}')"/>
          <button class="btn btn-sm" onclick="addInternalNote('${t.id}')">Add Note</button>
        </div>
      </div>
    </div>

    <div style="display:flex; flex-direction:column; gap:16px;">
      <div class="card">
        <div class="card-title">Assignee</div>
        <div>${assigneeDropdown}</div>
      </div>

      <div class="card" style="cursor:pointer;" onclick="navigate('customer-profile',{id:'${c.id}'})">
        <div class="card-title">Customer</div>
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
          <div class="avatar" style="width:38px;height:38px; font-size:13px;">${c.name.split(' ').map(x=>x[0]).join('')}</div>
          <div>
            <div style="font-weight:700; font-size:13.5px;">${c.name}</div>
            <div style="font-size:11.5px; color:var(--text-faint);">${c.plan}</div>
          </div>
        </div>
        <div style="font-size:12px; color:var(--text-muted); display:flex; flex-direction:column; gap:4px;">
          <div>${c.email}</div>
          <div>${c.phone}</div>
          <div>Customer since ${c.since}</div>
        </div>
      </div>
      <div class="card">
        <div class="card-title">Ticket History</div>
        <div class="timeline">
          ${historyList.map((item, idx) => `
            <div class="timeline-item" ${idx === historyList.length - 1 ? 'style="padding-bottom:0;"' : ''}>
              <div class="timeline-time">${item.time}</div>
              <div class="timeline-text">${item.text}</div>
            </div>
          `).join('')}
        </div>
      </div>
      <div class="card">
        <div class="card-title">Suggested Articles</div>
        <a class="nav-item" style="padding:8px 6px;" onclick="navigate('kb-article',{id:'kb2'})">${icon('book',15)} Understanding your monthly invoice</a>
        <a class="nav-item" style="padding:8px 6px;" onclick="navigate('kb-article',{id:'kb5'})">${icon('book',15)} Updating your payment method</a>
      </div>
    </div>
  </div>`;
}

// Interactivity helper functions
function useSuggestedReply(btn) {
  const text = btn.previousElementSibling.innerText.replace(/^"|"$/g, '');
  const textarea = document.getElementById('reply-textarea');
  if (textarea) {
    textarea.value = text;
  }
}

function sendAgentReply(ticketId) {
  const textarea = document.getElementById('reply-textarea');
  if (!textarea || !textarea.value.trim()) return;
  const replyText = textarea.value.trim();
  const t = TICKETS.find(x => x.id === ticketId);
  if (t) {
    if (!t.messages) t.messages = [];
    t.messages.push({ role: 'agent', text: replyText, timestamp: 'Just now' });
    if (!t.history) t.history = [];
    t.history.push({ time: 'Just now', text: 'Agent replied' });
    t.updated = 'Just now';
    render();
  }
}

function addInternalNote(ticketId) {
  const input = document.getElementById('note-input');
  if (!input || !input.value.trim()) return;
  const noteText = input.value.trim();
  const t = TICKETS.find(x => x.id === ticketId);
  if (t) {
    const timestampStr = 'You, Just now';
    t.notes = t.notes ? `${t.notes}<br/>${noteText} — ${timestampStr}` : `${noteText} — ${timestampStr}`;
    render();
  }
}

function assignTicket(ticketId, agentId) {
  const t = TICKETS.find(x => x.id === ticketId);
  if (t) {
    t.agent = agentId || null;
    if (!t.history) t.history = [];
    const agentName = agentId ? AGENTS.find(a => a.id === agentId).name : 'Unassigned';
    t.history.push({ time: 'Just now', text: `Ticket assigned to ${agentName}` });
    t.updated = 'Just now';
    render();
  }
}

function sendCustomerReply(ticketId) {
  const input = document.getElementById('customer-reply-input');
  if (!input || !input.value.trim()) return;
  const replyText = input.value.trim();
  const t = TICKETS.find(x => x.id === ticketId);
  if (t) {
    if (!t.messages) t.messages = [];
    t.messages.push({ role: 'customer', text: replyText, timestamp: 'Just now' });
    if (!t.history) t.history = [];
    t.history.push({ time: 'Just now', text: 'Customer replied' });
    t.status = 'Open';
    t.updated = 'Just now';
    render();
  }
}

function v_customerProfile(p){
  const c = custById(p.id) || CUSTOMERS.john;
  const hist = TICKETS.filter(t=>t.customer===c.id);
  return `
  <div class="breadcrumb"><a onclick="navigate('unified-inbox')">All Messages</a> / Customer Profile</div>
  <div class="grid" style="grid-template-columns:1fr 2fr; align-items:start;">
    <div class="card" style="text-align:center;">
      <div class="avatar" style="width:60px;height:60px; font-size:20px; margin:0 auto 10px auto;">${c.name.split(' ').map(x=>x[0]).join('')}</div>
      <div style="font-weight:800; font-size:15.5px;">${c.name}</div>
      <div style="font-size:12px; color:var(--text-faint); margin-bottom:14px;">${c.plan} · ${c.location}</div>
      <div style="text-align:left; font-size:12.5px; color:var(--text-muted); display:flex; flex-direction:column; gap:6px; margin-bottom:14px;">
        <div>${icon('mail',13)} &nbsp;${c.email}</div>
        <div>${icon('phone',13)} &nbsp;${c.phone}</div>
        <div>${icon('clock',13)} &nbsp;Customer since ${c.since}</div>
      </div>
      <div style="display:flex; gap:10px; justify-content:center;">
        <div><div style="font-family:var(--font-display); font-weight:800; font-size:18px;">${c.tickets}</div><div style="font-size:10.5px; color:var(--text-faint);">Tickets</div></div>
        <div><div style="font-family:var(--font-display); font-weight:800; font-size:18px; color:var(--success);">${c.csat}</div><div style="font-size:10.5px; color:var(--text-faint);">Avg CSAT</div></div>
      </div>
    </div>
    <div style="display:flex; flex-direction:column; gap:16px;">
      <div class="card">
        <div class="card-title">Customer Timeline</div>
        <div class="timeline">
          <div class="timeline-item"><div class="timeline-time">${c.since}</div><div class="timeline-text">Signed up for ${c.plan}</div></div>
          <div class="timeline-item"><div class="timeline-time">3 months ago</div><div class="timeline-text">Upgraded plan and added 2 team seats</div></div>
          <div class="timeline-item"><div class="timeline-time">This week</div><div class="timeline-text">Opened ${hist.length} support ticket(s)</div></div>
          <div class="timeline-item" style="padding-bottom:0;"><div class="timeline-time">Today</div><div class="timeline-text">Chatted with AI Assistant, escalated to agent</div></div>
        </div>
      </div>
      <div class="card">
        <div class="card-title">Tickets from ${c.name}</div>
        ${ticketTable(hist)}
      </div>
    </div>
  </div>`;
}

function v_macros(){
  const macros = [
    {name:'Refund Processed', cat:'Billing', text:'Your refund has been processed and should appear in 5-7 business days.'},
    {name:'Order Shipped', cat:'Orders', text:'Great news — your order has shipped! Tracking details are on their way to your inbox.'},
    {name:'Password Reset Sent', cat:'Account', text:'I\'ve sent a password reset link to your registered email, valid for 30 minutes.'},
    {name:'Escalation Notice', cat:'General', text:'I\'m looping in a specialist who can dig deeper into this for you — you\'ll hear back within 2 hours.'},
    {name:'CSAT Follow-up', cat:'General', text:'Glad we could help! We\'d love your feedback — a quick survey link is on its way.'},
    {name:'Shipping Delay Apology', cat:'Shipping', text:'Apologies for the delay — your courier is reporting a short hold, updated ETA is within 48 hours.'},
  ];
  return `
  <div class="section-title">Quick Replies</div>
  <div class="section-sub">Pre-written replies to answer common questions faster.</div>
  <div class="grid grid-3">
    ${macros.map(m=>`
      <div class="card">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:8px;">
          <div style="font-weight:700; font-size:13.5px;">${m.name}</div>
          <span class="chip">${m.cat}</span>
        </div>
        <div style="font-size:12.5px; color:var(--text-muted); line-height:1.5; margin-bottom:12px;">"${m.text}"</div>
        <button class="btn btn-sm" style="width:100%; justify-content:center;">Insert into reply</button>
      </div>
    `).join('')}
  </div>`;
}

function v_kbSearchAgent(){
  return `
  <div class="section-title">Help Center Search</div>
  <div class="section-sub">Search articles to answer customers faster, or share a link directly in a reply.</div>
  <div class="searchbox" style="width:100%; max-width:none; margin-bottom:22px; padding:13px 16px;">${icon('search',17)}<span>Search articles…</span></div>
  <div class="grid grid-2">
    ${KB_ARTICLES.map(a=>`
      <div class="card" style="cursor:pointer;" onclick="navigate('kb-article',{id:'${a.id}'})">
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
          <div style="font-weight:700; font-size:14px; margin-bottom:6px; max-width:80%;">${a.title}</div>
          <span class="chip">${a.cat}</span>
        </div>
        <div style="font-size:12px; color:var(--text-faint); margin-bottom:10px;">${a.views} views · ${a.helpful}% helpful</div>
        <button class="btn btn-sm">${icon('send',12)} Share with customer</button>
      </div>
    `).join('')}
  </div>`;
}

/* ============================================================
   SUPPORT MANAGER VIEWS
   ============================================================ */
function v_managerDashboard(){
  return `
  <div class="section-title">Support Overview</div>
  <div class="section-sub">Today's snapshot across all channels and agents.</div>
  <div class="grid grid-4" style="margin-bottom:20px;">
    ${kpi('ticket','Total Tickets','1,284','+8.2%',true,'#4F46E5')}
    ${kpi('check','Open vs Closed','62% closed','+3%',true,'#15803D')}
    ${kpi('clock','SLA Compliance (On-Time Replies)','94%','-1.5%',false,'#B45309')}
    ${kpi('bot','AI Resolution Rate','38%','+6%',true,'#9333EA')}
  </div>
  <div class="grid" style="grid-template-columns:1.4fr 1fr; align-items:start; margin-bottom:20px;">
    <div class="card">
      <div class="card-title">Tickets by Channel (7 days)</div>
      <div style="display:flex; align-items:flex-end; gap:18px; height:160px; padding:10px 6px 0 6px;">
        ${[['Email',482,'#0369A1'],['Website Chat',610,'#4F46E5'],['WhatsApp',295,'#15803D'],['Instagram',140,'#C026D3'],['Facebook',88,'#1D4ED8']].map(([n,v,col])=>`
          <div style="flex:1; text-align:center;">
            <div style="height:${Math.round(v/610*130)}px; background:${col}; border-radius:6px 6px 0 0; margin-bottom:8px;"></div>
            <div style="font-size:11px; font-weight:700;">${v}</div>
            <div style="font-size:10.5px; color:var(--text-faint);">${n}</div>
          </div>`).join('')}
      </div>
    </div>
    <div class="card">
      <div class="card-title">Customer Satisfaction</div>
      <div style="text-align:center; padding:6px 0 14px 0;">
        <div style="font-family:var(--font-display); font-size:38px; font-weight:800;">4.6</div>
        <div class="stars">★★★★★</div>
        <div style="font-size:11.5px; color:var(--text-faint); margin-top:4px;">from 1,042 responses</div>
      </div>
      <div class="stat-bar-row"><div class="stat-bar-label">Excellent</div><div class="stat-bar-track"><div class="stat-bar-fill" style="width:71%; background:var(--success);"></div></div><div class="stat-bar-val">71%</div></div>
      <div class="stat-bar-row"><div class="stat-bar-label">Good</div><div class="stat-bar-track"><div class="stat-bar-fill" style="width:20%; background:#4ADE80;"></div></div><div class="stat-bar-val">20%</div></div>
      <div class="stat-bar-row"><div class="stat-bar-label">Poor</div><div class="stat-bar-track"><div class="stat-bar-fill" style="width:9%; background:var(--danger);"></div></div><div class="stat-bar-val">9%</div></div>
    </div>
  </div>
  <div class="grid" style="grid-template-columns:1fr 1fr;">
    <div class="card">
      <div class="card-title">Agent Snapshot <a class="btn btn-ghost btn-sm" onclick="navigate('agent-performance')">Details ${icon('chev',13)}</a></div>
      ${AGENTS.map(a=>`
        <div style="display:flex; align-items:center; gap:10px; padding:9px 0; border-bottom:1px solid var(--border);">
          <span class="avatar-sm" style="background:${a.color}; width:30px;height:30px;">${a.initials}</span>
          <div style="flex:1;">
            <div style="font-size:13px; font-weight:700;">${a.name}</div>
            <div style="font-size:11px; color:var(--text-faint);">${a.tickets} active · CSAT ${a.csat}</div>
          </div>
          <span class="pill pill-resolved">${a.sla}% SLA</span>
        </div>`).join('')}
    </div>
    <div class="card">
      <div class="card-title">Recent Activity</div>
      ${NOTIFS.map(n=>`
        <div style="display:flex; gap:10px; padding:9px 0; border-bottom:1px solid var(--border); align-items:flex-start;">
          <span style="color:${n.color}; flex-shrink:0; margin-top:2px;">${icon(n.icon,15)}</span>
          <div style="flex:1;"><div style="font-size:12.5px; font-weight:600;">${n.text}</div><div style="font-size:11px; color:var(--text-faint);">${n.time}</div></div>
        </div>`).join('')}
    </div>
  </div>`;
}

function v_analytics(){
  return `
  <div class="section-title">Analytics</div>
  <div class="section-sub">Ticket volume, resolution trends and channel performance.</div>
  <div class="grid grid-4" style="margin-bottom:20px;">
    ${kpi('ticket','Tickets This Month','1,284','+8.2%',true,'#4F46E5')}
    ${kpi('clock','Avg. First Response','11m 40s','-2m',true,'#0369A1')}
    ${kpi('check','Avg. Resolution Time','2h 15m','-18m',true,'#15803D')}
    ${kpi('smile','CSAT','4.6 / 5','+0.2',true,'#9333EA')}
  </div>
  <div class="card" style="margin-bottom:20px;">
    <div class="card-title">Ticket Volume — Last 14 Days</div>
    <div style="display:flex; align-items:flex-end; gap:8px; height:150px; padding-top:10px;">
      ${[38,44,40,52,60,48,55,62,58,66,70,64,72,68].map(v=>`<div style="flex:1; background:linear-gradient(180deg,#818CF8,#4F46E5); border-radius:5px 5px 0 0; height:${v}%;"></div>`).join('')}
    </div>
  </div>
  <div class="grid grid-2">
    <div class="card">
      <div class="card-title">Tickets by Category</div>
      ${[['Billing',32,'#4F46E5'],['Technical',26,'#0EA5E9'],['Orders',20,'#9333EA'],['Refund',13,'#DB2777'],['Shipping',9,'#15803D']].map(([n,v,c])=>`
        <div class="stat-bar-row"><div class="stat-bar-label">${n}</div><div class="stat-bar-track"><div class="stat-bar-fill" style="width:${v*3}%; background:${c};"></div></div><div class="stat-bar-val">${v}%</div></div>
      `).join('')}
    </div>
    <div class="card">
      <div class="card-title">AI vs Human Resolution</div>
      <div style="display:flex; align-items:center; gap:20px; padding:10px 0;">
        <svg width="120" height="120" viewBox="0 0 36 36">
          <circle cx="18" cy="18" r="15.9" fill="none" stroke="#EEF0FA" stroke-width="4"/>
          <circle cx="18" cy="18" r="15.9" fill="none" stroke="#9333EA" stroke-width="4" stroke-dasharray="38 62" stroke-dashoffset="25" stroke-linecap="round"/>
          <circle cx="18" cy="18" r="15.9" fill="none" stroke="#4F46E5" stroke-width="4" stroke-dasharray="62 38" stroke-dashoffset="87" stroke-linecap="round"/>
        </svg>
        <div>
          <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;"><span style="width:10px;height:10px;border-radius:3px; background:#9333EA;"></span><span style="font-size:12.5px; font-weight:700;">AI Resolved — 38%</span></div>
          <div style="display:flex; align-items:center; gap:8px;"><span style="width:10px;height:10px;border-radius:3px; background:#4F46E5;"></span><span style="font-size:12.5px; font-weight:700;">Agent Resolved — 62%</span></div>
        </div>
      </div>
    </div>
  </div>`;
}

function v_agentPerformance(){
  return `
  <div class="section-title">Agent Performance</div>
  <div class="section-sub">Compare workload, quality and speed across the team.</div>
  <div class="card" style="padding:0; margin-bottom:20px;">
    <table>
      <thead><tr><th>Agent</th><th>Active Tickets</th><th>Resolved (30d)</th><th>Avg. Handle Time</th><th>SLA Compliance</th><th>CSAT</th></tr></thead>
      <tbody>
        ${AGENTS.map(a=>`
          <tr class="tbl-row">
            <td><div style="display:flex; align-items:center; gap:9px;"><span class="avatar-sm" style="background:${a.color}; width:30px;height:30px;">${a.initials}</span><div><div style="font-weight:700;">${a.name}</div><div style="font-size:11px; color:var(--text-faint);">${a.title}</div></div></div></td>
            <td>${a.tickets}</td>
            <td>${a.resolved}</td>
            <td>${a.avgHandle}</td>
            <td><div style="display:flex; align-items:center; gap:8px;"><div class="progress-track" style="width:70px;"><div class="progress-fill" style="width:${a.sla}%; background:${a.sla>90?'var(--success)':'var(--warning)'};"></div></div>${a.sla}%</div></td>
            <td><span class="stars" style="font-size:12px;">★</span> ${a.csat}</td>
          </tr>`).join('')}
      </tbody>
    </table>
  </div>
  <div class="grid grid-3">
    ${AGENTS.map(a=>`
      <div class="card">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">
          <span class="avatar-sm" style="background:${a.color}; width:34px;height:34px;">${a.initials}</span>
          <div><div style="font-weight:700; font-size:13.5px;">${a.name}</div><div style="font-size:11px; color:var(--text-faint);">${a.title}</div></div>
        </div>
        <div class="stat-bar-row"><div class="stat-bar-label">SLA</div><div class="stat-bar-track"><div class="stat-bar-fill" style="width:${a.sla}%; background:var(--primary);"></div></div><div class="stat-bar-val">${a.sla}%</div></div>
        <div class="stat-bar-row"><div class="stat-bar-label">CSAT</div><div class="stat-bar-track"><div class="stat-bar-fill" style="width:${a.csat/5*100}%; background:var(--success);"></div></div><div class="stat-bar-val">${a.csat}</div></div>
      </div>
    `).join('')}
  </div>`;
}

function v_slaDashboard(){
  const atRisk = TICKETS.filter(t=>t.slaState==='warn'||t.slaState==='bad');
  return `
  <div class="section-title">SLA Dashboard</div>
  <div class="section-sub">Track response and resolution commitments in real time.</div>
  <div class="grid grid-4" style="margin-bottom:20px;">
    ${kpi('check','Overall Compliance','94%','-1.5%',false,'#15803D')}
    ${kpi('clock','First Response SLA','96%','+0.5%',true,'#0369A1')}
    ${kpi('check','Resolution SLA','91%','-2%',false,'#4F46E5')}
    ${kpi('alert','Tickets At Risk', atRisk.length.toString(), null, false, '#DC2626')}
  </div>
  <div class="card" style="margin-bottom:20px;">
    <div class="card-title">Tickets At Risk of Breach</div>
    ${ticketTable(atRisk)}
  </div>
  <div class="card">
    <div class="card-title">SLA by Priority Tier</div>
    ${[['Urgent — 1 hr response',88,'var(--danger)'],['High — 4 hr response',93,'#C2410C'],['Medium — 8 hr response',96,'var(--warning)'],['Low — 24 hr response',99,'var(--success)']].map(([n,v,c])=>`
      <div class="stat-bar-row"><div class="stat-bar-label" style="width:180px;">${n}</div><div class="stat-bar-track"><div class="stat-bar-fill" style="width:${v}%; background:${c};"></div></div><div class="stat-bar-val">${v}%</div></div>
    `).join('')}
  </div>`;
}

function v_ticketReports(){
  return `
  <div class="section-title">Ticket Reports</div>
  <div class="section-sub">Generate and export reports for stakeholders.</div>
  <div style="display:flex; gap:10px; margin-bottom:18px;">
    <button class="btn btn-primary btn-sm">${icon('download',13)} Export CSV</button>
    <button class="btn btn-sm">${icon('download',13)} Export PDF</button>
    <button class="btn btn-sm" style="margin-left:auto;">${icon('filter',13)} Last 30 days</button>
  </div>
  <div class="grid grid-3" style="margin-bottom:20px;">
    ${kpi('ticket','Tickets Created','1,284',null,true,'#4F46E5')}
    ${kpi('check','Tickets Resolved','1,198',null,true,'#15803D')}
    ${kpi('clock','Avg Resolution','2h 15m',null,true,'#0369A1')}
  </div>
  <div class="card" style="padding:0;">
    <table>
      <thead><tr><th>Ticket</th><th>Customer</th><th>Category</th><th>Status</th><th>Agent</th><th>Created</th></tr></thead>
      <tbody>
        ${TICKETS.map(t=>`<tr class="tbl-row" onclick="navigate('ticket-details',{id:'${t.id}'})">
          <td class="mono">${t.id}</td><td>${custById(t.customer).name}</td><td>${t.category}</td><td>${statusPill(t.status)}</td><td>${fmtAgent(t.agent)}</td><td>${t.created}</td>
        </tr>`).join('')}
      </tbody>
    </table>
  </div>`;
}

function v_workflowAutomation(){
  const Step = (label, sub, aiFlag) => `
    <div class="workflow-step ${aiFlag?'ai':''}">
      <div class="ai-glow-icon" style="width:32px;height:32px;border-radius:9px; ${aiFlag?'':'background:var(--primary);'}">${icon(aiFlag?'sparkle':'check',16)}</div>
      <div><div style="font-weight:700; font-size:13px;">${label}</div><div style="font-size:11px; color:var(--text-faint);">${sub}</div></div>
    </div>`;
  const Arrow = `<div class="workflow-arrow">${icon('arrowDown',20)}</div>`;
  return `
  <div class="section-title">Workflow Automation</div>
  <div class="section-sub">How a customer message flows from first contact to a closed, analyzed ticket.</div>
  <div class="card" style="display:flex; flex-direction:column; align-items:center; padding:32px;">
    ${Step('Customer Message','Sent via Email, Chat, WhatsApp, Instagram or Facebook', false)}
    ${Arrow}
    ${Step('Message Received','Logged and routed by channel', false)}
    ${Arrow}
    ${Step('All Messages','Appears alongside every other conversation', false)}
    ${Arrow}
    ${Step('AI Knowledge Search','AI scans the Help Center for a relevant answer', true)}
    ${Arrow}
    ${Step('AI Reply','A draft or live answer is generated for the customer', true)}
    ${Arrow}
    ${Step('Confidence Check','AI scores its own certainty in the answer', true)}
    ${Arrow}
    <div class="workflow-branch">
      <div style="text-align:center;">
        ${Step('Resolved','Customer confirms — ticket closes automatically', false)}
      </div>
      <div style="text-align:center;">
        ${Step('Escalate to Agent','Low confidence or explicit request routes to a human', false)}
        ${Arrow}
        ${Step('Agent Reply','Agent responds using AI-suggested replies & quick replies', false)}
      </div>
    </div>
    ${Arrow}
    ${Step('Ticket Closed','Marked resolved by agent or automatically', false)}
    ${Arrow}
    ${Step('CSAT Survey','Customer is asked to rate the experience', false)}
    ${Arrow}
    ${Step('Analytics Updated','Dashboards refresh with the new outcome', false)}
  </div>
  <div class="grid grid-3" style="margin-top:20px;">
    <div class="card">
      <div class="card-title">Active Automations</div>
      <div class="settings-row"><div><div class="settings-label">Auto-route by keyword</div><div class="settings-sub">Billing keywords → Billing queue</div></div><div class="switch on"></div></div>
      <div class="settings-row"><div><div class="settings-label">Auto-escalate after 4h idle</div><div class="settings-sub">Waiting tickets notify manager</div></div><div class="switch on"></div></div>
      <div class="settings-row"><div><div class="settings-label">Auto-close after CSAT</div><div class="settings-sub">Closes 24h after resolved</div></div><div class="switch"></div></div>
    </div>
    <div class="card">
      <div class="card-title">This Week</div>
      <div class="stat-bar-row"><div class="stat-bar-label">Auto-resolved</div><div class="stat-bar-track"><div class="stat-bar-fill" style="width:38%; background:#9333EA;"></div></div><div class="stat-bar-val">38%</div></div>
      <div class="stat-bar-row"><div class="stat-bar-label">Auto-routed</div><div class="stat-bar-track"><div class="stat-bar-fill" style="width:82%; background:var(--primary);"></div></div><div class="stat-bar-val">82%</div></div>
      <div class="stat-bar-row"><div class="stat-bar-label">Auto-escalated</div><div class="stat-bar-track"><div class="stat-bar-fill" style="width:12%; background:var(--warning);"></div></div><div class="stat-bar-val">12%</div></div>
    </div>
    <div class="card">
      <div class="card-title">Add New Automation</div>
      <div style="font-size:12.5px; color:var(--text-muted); margin-bottom:12px;">Trigger an action automatically when a condition is met.</div>
      <button class="btn btn-primary" style="width:100%; justify-content:center;">${icon('plus',14)} Create Automation</button>
    </div>
  </div>`;
}

/* ============================================================
   ADMIN VIEWS
   ============================================================ */
const SYSTEM_USERS = [
  {name:'Emma Wilson', email:'emma.wilson@supporthub.com', role:'Support Agent', status:'Active', last:'2 min ago'},
  {name:'David Brown', email:'david.brown@supporthub.com', role:'Support Agent', status:'Active', last:'18 min ago'},
  {name:'Alex Thomas', email:'alex.thomas@supporthub.com', role:'Support Agent', status:'Active', last:'1 hr ago'},
  {name:'Olivia Reyes', email:'olivia.reyes@supporthub.com', role:'Support Manager', status:'Active', last:'5 min ago'},
  {name:'Marcus Lee', email:'marcus.lee@supporthub.com', role:'Admin', status:'Active', last:'Just now'},
  {name:'Nina Cole', email:'nina.cole@supporthub.com', role:'Support Agent', status:'Invited', last:'—'},
];

function v_adminDashboard(){
  return `
  <div class="section-title">Admin Overview</div>
  <div class="section-sub">System health, users and integrations at a glance.</div>
  <div class="grid grid-4" style="margin-bottom:20px;">
    ${kpi('users','Total Users','24','+2',true,'#4F46E5')}
    ${kpi('plug','Connected Channels','4 / 5',null,true,'#0EA5E9')}
    ${kpi('book','KB Articles','48','+3',true,'#9333EA')}
    ${kpi('bot','AI Auto-Resolution','38%','+6%',true,'#15803D')}
  </div>
  <div class="grid" style="grid-template-columns:1.3fr 1fr; align-items:start;">
    <div class="card">
      <div class="card-title">Recent Users <a class="btn btn-ghost btn-sm" onclick="navigate('user-management')">Manage ${icon('chev',13)}</a></div>
      <table>
        <thead><tr><th>Name</th><th>Role</th><th>Status</th><th>Last Active</th></tr></thead>
        <tbody>${SYSTEM_USERS.slice(0,5).map(u=>`<tr><td><div style="font-weight:700;">${u.name}</div><div style="font-size:11px; color:var(--text-faint);">${u.email}</div></td><td>${u.role}</td><td><span class="pill ${u.status==='Active'?'pill-resolved':'pill-waiting'}">${u.status}</span></td><td style="color:var(--text-faint);">${u.last}</td></tr>`).join('')}</tbody>
      </table>
    </div>
    <div class="card">
      <div class="card-title">Channel Status</div>
      ${CHANNELS.map(c=>`
        <div style="display:flex; align-items:center; gap:10px; padding:9px 0; border-bottom:1px solid var(--border);">
          <span style="color:${CH_COLOR[c.name]||'var(--primary)'};">${icon(c.icon,17)}</span>
          <div style="flex:1;"><div style="font-size:13px; font-weight:700;">${c.name}</div><div style="font-size:11px; color:var(--text-faint);">${c.detail}</div></div>
          <span class="pill ${c.status==='Connected'?'pill-resolved':'pill-waiting'}">${c.status}</span>
        </div>`).join('')}
    </div>
  </div>`;
}

function v_userManagement(){
  return `
  <div class="section-title">User Management</div>
  <div class="section-sub">Manage everyone who can access SupportHub.</div>
  <div style="display:flex; justify-content:space-between; margin-bottom:16px;">
    <div class="searchbox" style="width:280px;">${icon('search',15)}<span>Search users…</span></div>
    <button class="btn btn-primary">${icon('plus',14)} Invite User</button>
  </div>
  <div class="card" style="padding:0;">
    <table>
      <thead><tr><th>Name</th><th>Email</th><th>Role</th><th>Status</th><th>Last Active</th><th></th></tr></thead>
      <tbody>
        ${SYSTEM_USERS.map(u=>`
          <tr class="tbl-row">
            <td><div style="display:flex; align-items:center; gap:9px;"><span class="avatar-sm" style="width:28px;height:28px;">${u.name.split(' ').map(x=>x[0]).join('')}</span><b>${u.name}</b></div></td>
            <td style="color:var(--text-faint);">${u.email}</td>
            <td>${u.role}</td>
            <td><span class="pill ${u.status==='Active'?'pill-resolved':'pill-waiting'}">${u.status}</span></td>
            <td style="color:var(--text-faint);">${u.last}</td>
            <td><button class="btn btn-sm">Edit</button></td>
          </tr>`).join('')}
      </tbody>
    </table>
  </div>`;
}

function v_channelIntegrations(){
  return `
  <div class="section-title">Channel Integrations</div>
  <div class="section-sub">Connect the channels your customers use to reach you.</div>
  <div class="grid grid-3">
    ${CHANNELS.map(c=>`
      <div class="card">
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:12px;">
          <span class="ai-glow-icon" style="background:${CH_COLOR[c.name]||'var(--primary)'}; width:38px;height:38px;border-radius:10px;">${icon(c.icon,18)}</span>
          <span class="pill ${c.status==='Connected'?'pill-resolved':'pill-waiting'}">${c.status}</span>
        </div>
        <div style="font-weight:700; font-size:14.5px; margin-bottom:3px;">${c.name}</div>
        <div style="font-size:12px; color:var(--text-faint); margin-bottom:4px;">${c.detail}</div>
        <div style="font-size:12px; color:var(--text-muted); margin-bottom:14px;">${c.volume} messages</div>
        <button class="btn btn-sm" style="width:100%; justify-content:center;">${c.status==='Connected'?'Manage':'Connect'}</button>
      </div>
    `).join('')}
    <div class="card" style="display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; border-style:dashed;">
      <div class="ai-glow-icon" style="background:var(--surface-alt); color:var(--text-faint); width:38px;height:38px;border-radius:10px; margin-bottom:10px;">${icon('plus',18)}</div>
      <div style="font-weight:700; font-size:13.5px; margin-bottom:4px;">Add a channel</div>
      <div style="font-size:12px; color:var(--text-faint);">SMS, Slack, Telegram & more</div>
    </div>
  </div>`;
}

function v_kbManagement(){
  return `
  <div class="section-title">Help Center Management</div>
  <div class="section-sub">Create and maintain the articles your AI and agents rely on.</div>
  <div style="display:flex; justify-content:space-between; margin-bottom:16px;">
    <div class="searchbox" style="width:280px;">${icon('search',15)}<span>Search articles…</span></div>
    <button class="btn btn-primary">${icon('plus',14)} New Article</button>
  </div>
  <div class="card" style="padding:0;">
    <table>
      <thead><tr><th>Article</th><th>Category</th><th>Views</th><th>Helpful</th><th>Updated</th><th></th></tr></thead>
      <tbody>
        ${KB_ARTICLES.map(a=>`
          <tr class="tbl-row" onclick="navigate('kb-article',{id:'${a.id}'})">
            <td><b>${a.title}</b></td><td><span class="chip">${a.cat}</span></td><td>${a.views}</td><td>${a.helpful}%</td><td style="color:var(--text-faint);">${a.updated}</td>
            <td><button class="btn btn-sm">Edit</button></td>
          </tr>`).join('')}
      </tbody>
    </table>
  </div>`;
}

function v_aiSettings(){
  return `
  <div class="section-title">AI Settings</div>
  <div class="section-sub">Control how the AI Assistant responds, escalates and learns.</div>
  <div class="grid" style="grid-template-columns:1.4fr 1fr; align-items:start;">
    <div class="card">
      <div class="card-title">Behavior</div>
      <div class="settings-row"><div><div class="settings-label">Enable AI Assistant</div><div class="settings-sub">Let customers get instant AI answers</div></div><div class="switch on"></div></div>
      <div class="settings-row"><div><div class="settings-label">Auto-resolve high-confidence answers</div><div class="settings-sub">Close tickets automatically above the confidence threshold</div></div><div class="switch on"></div></div>
      <div class="settings-row"><div><div class="settings-label">AI reply suggestions for agents</div><div class="settings-sub">Show suggested replies inside ticket details</div></div><div class="switch on"></div></div>
      <div class="settings-row"><div><div class="settings-label">AI ticket summaries</div><div class="settings-sub">Summarize conversations for agents automatically</div></div><div class="switch on"></div></div>
      <div class="settings-row"><div><div class="settings-label">Sentiment detection</div><div class="settings-sub">Flag frustrated customers for priority handling</div></div><div class="switch on"></div></div>
      <div style="margin-top:16px;">
        <div class="settings-label" style="margin-bottom:8px;">Confidence threshold to auto-resolve</div>
        <div class="progress-track" style="height:9px;"><div class="progress-fill" style="width:85%; background:var(--ai-grad, #9333EA);"></div></div>
        <div style="display:flex; justify-content:space-between; font-size:11px; color:var(--text-faint); margin-top:4px;"><span>0%</span><span style="font-weight:700; color:var(--text);">85%</span><span>100%</span></div>
      </div>
    </div>
    <div class="card">
      <div class="card-title">Model & Sources</div>
      <div style="font-size:12.5px; color:var(--text-muted); margin-bottom:12px;">The AI answers using content from your connected sources.</div>
      <div class="chip" style="margin-bottom:8px; display:flex;">${icon('book',13)} Help Center — 48 articles</div><br/>
      <div class="chip" style="margin-bottom:8px; display:flex;">${icon('ticket',13)} Past resolved tickets — 1,198</div><br/>
      <div class="chip" style="display:flex;">${icon('mail',13)} FAQ documents — 6 files</div>
      <div style="margin-top:16px; padding-top:14px; border-top:1px solid var(--border);">
        <div class="settings-label" style="margin-bottom:6px;">Escalation rule</div>
        <div style="font-size:12.5px; color:var(--text-muted);">If confidence is below threshold, or the customer says "talk to a human", route to the next available agent.</div>
      </div>
    </div>
  </div>`;
}

function v_rolesPermissions(){
  const roles = [
    {name:'Customer', perms:['View own tickets','Chat with AI Assistant','Browse Help Center']},
    {name:'Support Agent', perms:['View all messages','Reply to tickets','Use AI suggestions & quick replies','View customer profiles']},
    {name:'Support Manager', perms:['All Agent permissions','View analytics & reports','Manage SLA rules','Configure workflow automation']},
    {name:'Admin', perms:['All Manager permissions','Manage users & roles','Manage channel integrations','Configure AI settings','Manage system settings']},
  ];
  return `
  <div class="section-title">Roles & Permissions</div>
  <div class="section-sub">Define what each role can see and do inside SupportHub.</div>
  <div class="grid grid-2">
    ${roles.map(r=>`
      <div class="card">
        <div class="card-title">${r.name} <span class="chip">${r.perms.length} permissions</span></div>
        <div style="display:flex; flex-direction:column; gap:9px;">
          ${r.perms.map(p=>`<div style="display:flex; align-items:center; gap:8px; font-size:12.5px;"><span style="color:var(--success);">${icon('check',14)}</span>${p}</div>`).join('')}
        </div>
      </div>
    `).join('')}
  </div>`;
}

function v_systemSettings(){
  return `
  <div class="section-title">System Settings</div>
  <div class="section-sub">General configuration for your SupportHub workspace.</div>
  <div class="grid" style="grid-template-columns:1.4fr 1fr; align-items:start;">
    <div class="card" style="margin-bottom:16px;">
      <div class="card-title">Workspace</div>
      <div class="settings-row"><div><div class="settings-label">Workspace name</div><div class="settings-sub">Shown across the customer portal</div></div><div class="chip">Brand Inc.</div></div>
      <div class="settings-row"><div><div class="settings-label">Time zone</div><div class="settings-sub">Used for SLA timers and reports</div></div><div class="chip">${icon('clock',12)} GMT+5:30 Kolkata</div></div>
      <div class="settings-row"><div><div class="settings-label">Business hours</div><div class="settings-sub">Mon–Fri, 9:00 AM – 7:00 PM</div></div><div class="switch on"></div></div>
      <div class="settings-row"><div><div class="settings-label">Default language</div><div class="settings-sub">Used for AI replies and templates</div></div><div class="chip">English</div></div>
    </div>
    <div class="card">
      <div class="card-title">Security</div>
      <div class="settings-row"><div><div class="settings-label">Two-factor authentication</div><div class="settings-sub">Required for Admin & Manager roles</div></div><div class="switch on"></div></div>
      <div class="settings-row"><div><div class="settings-label">Single sign-on (SSO)</div><div class="settings-sub">Google Workspace connected</div></div><div class="switch on"></div></div>
      <div class="settings-row"><div><div class="settings-label">Session timeout</div><div class="settings-sub">Auto sign-out after inactivity</div></div><div class="chip">${icon('key',12)} 30 min</div></div>
    </div>
  </div>`;
}

/* ============================================================
   VIEW REGISTRY + BOOTSTRAP
   ============================================================ */
function v_ticketDetails(p){
  const t = TICKETS.find(x=>x.id===p.id) || TICKETS[0];
  const c = custById(t.customer);
  return STATE.role === 'customer' ? v_ticketDetailsCustomer(t,c) : v_ticketDetailsAgent(t,c);
}

const VIEWS = {
  // customer
  'customer-portal': v_customerPortal,
  'my-tickets': v_myTickets,
  'live-chat': v_liveChat,
  'ai-chatbot': v_aiChatbot,
  'knowledge-base': v_knowledgeBase,
  'kb-article': v_kbArticle,
  'profile': v_profile,
  'ticket-details': v_ticketDetails,
  // agent
  'agent-dashboard': v_agentDashboard,
  'unified-inbox': v_unifiedInbox,
  'ticket-queue': v_ticketQueue,
  'customer-profile': v_customerProfile,
  'macros': v_macros,
  'kb-search': v_kbSearchAgent,
  // manager
  'manager-dashboard': v_managerDashboard,
  'analytics': v_analytics,
  'agent-performance': v_agentPerformance,
  'sla-dashboard': v_slaDashboard,
  'ticket-reports': v_ticketReports,
  'workflow-automation': v_workflowAutomation,
  // admin
  'admin-dashboard': v_adminDashboard,
  'user-management': v_userManagement,
  'channel-integrations': v_channelIntegrations,
  'kb-management': v_kbManagement,
  'ai-settings': v_aiSettings,
  'roles-permissions': v_rolesPermissions,
  'system-settings': v_systemSettings,
};

/* ---------------- Init ---------------- */
render();
