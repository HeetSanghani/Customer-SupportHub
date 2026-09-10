import { Paperclip, Send, User as UserIcon } from 'lucide-react'
import client from '../../api/client'

export function renderFormattedContent(text, isMe = false) {
  if (!text) return null

  const lines = text.split('\n')

  return (
    <div className="space-y-1 leading-relaxed">
      {lines.map((line, lineIdx) => {
        const trimmed = line.trim()
        if (!trimmed) {
          return <div key={lineIdx} className="h-1.5" />
        }

        const isBullet = /^[•\-*]\s+/.test(trimmed)
        const lineContent = isBullet ? trimmed.replace(/^[•\-*]\s+/, '') : line

        const parseInline = (str) => {
          const parts = []
          let lastIdx = 0
          const regex = /(\*\*(.*?)\*\*|\*(.*?)\*|`([^`]+)`)/g
          let match

          while ((match = regex.exec(str)) !== null) {
            if (match.index > lastIdx) {
              parts.push(str.substring(lastIdx, match.index))
            }

            if (match[2] !== undefined) {
              parts.push(
                <strong key={match.index} className="font-extrabold text-inherit">
                  {match[2]}
                </strong>
              )
            } else if (match[3] !== undefined) {
              parts.push(
                <em key={match.index} className="italic text-inherit">
                  {match[3]}
                </em>
              )
            } else if (match[4] !== undefined) {
              parts.push(
                <code
                  key={match.index}
                  className={`px-1.5 py-0.5 mx-0.5 rounded font-mono text-[11px] font-bold inline-block border ${
                    isMe
                      ? 'bg-white/20 text-white border-white/30'
                      : 'bg-indigo-50 text-indigo-700 border-indigo-200/80'
                  }`}
                >
                  {match[4]}
                </code>
              )
            }
            lastIdx = regex.lastIndex
          }

          if (lastIdx < str.length) {
            parts.push(str.substring(lastIdx))
          }

          return parts.length > 0 ? parts : str
        }

        if (isBullet) {
          return (
            <div key={lineIdx} className="flex items-start gap-2 my-0.5 pl-0.5">
              <span className={`font-bold shrink-0 mt-0.5 text-xs ${isMe ? 'text-white' : 'text-indigo-500'}`}>•</span>
              <span className="flex-1">{parseInline(lineContent)}</span>
            </div>
          )
        }

        return (
          <div key={lineIdx} className="leading-relaxed">
            {parseInline(line)}
          </div>
        )
      })}
    </div>
  )
}

/**
 * Renders a single message body — handles text, images, video, audio, PDF, and generic files.
 */
export function MessageBody({ msg, isMe }) {
  const body = msg.body || ''
  const match = body.match(/📎\s*\[Attachment:\s*([^\]]+)\]\(([^)]+)\)/i) ||
                body.match(/📎\s*Attachment:\s*([^\s(]+)\s*\(([^)]+)\)/i)

  if (match) {
    const filename = match[1]
    let rawUrl = match[2]
    const base = (window.location.port==='5173'||window.location.port==='3000') ? 'http://localhost:8000' : ''
    const url = rawUrl.startsWith('http') ? rawUrl : `${base}${rawUrl.startsWith('/')?'':'/'}${rawUrl}`
    const isImg   = /\.(jpg|jpeg|png|gif|webp|svg|bmp)(\?.*)?$/i.test(filename+url) || /(fbsbx|fbcdn|cdninstagram)/i.test(url)
    const isVid   = /\.(mp4|webm|ogg|mov|avi)(\?.*)?$/i.test(filename+url)
    const isAudio = /\.(mp3|wav|ogg|m4a|aac)(\?.*)?$/i.test(filename+url)
    const isPdf   = /\.pdf(\?.*)?$/i.test(filename+url)
    const rest    = body.replace(match[0],'').trim()
    return (
      <div className="space-y-2">
        {isImg && <a href={url} target="_blank" rel="noopener noreferrer" className="block max-w-xs rounded-xl overflow-hidden border border-white/20">
          <img src={url} alt={filename} className="w-full h-auto max-h-48 object-cover"
            onError={e=>{e.target.style.display='none'}} /></a>}
        {isVid && <div className="max-w-xs rounded-xl overflow-hidden bg-black border border-white/20">
          <video controls preload="metadata" className="w-full h-auto max-h-48" src={url} /></div>}
        {isAudio && <div className="max-w-xs p-2 rounded-xl bg-black/10 border border-white/20">
          <audio controls className="w-full h-8" src={url} />
          <div className="text-[10px] opacity-70 mt-1 truncate">🎵 {filename}</div></div>}
        {isPdf && <a href={url} target="_blank" rel="noopener noreferrer"
          className="inline-flex items-center gap-2 px-3 py-2 bg-rose-50 hover:bg-rose-100 border border-rose-200 text-rose-800 rounded-xl text-xs font-bold">
          📄 {filename}</a>}
        {!isImg&&!isVid&&!isAudio&&!isPdf && <a href={url} target="_blank" rel="noopener noreferrer"
          className="inline-flex items-center gap-2 px-3 py-1.5 bg-black/10 hover:bg-black/20 rounded-xl text-xs font-bold underline">
          📎 {filename}</a>}
        {rest && <div className="text-sm leading-relaxed">{renderFormattedContent(rest, isMe)}</div>}
      </div>
    )
  }
  if (msg.body_html) return <div className="text-sm leading-relaxed prose prose-sm max-w-none" dangerouslySetInnerHTML={{__html:msg.body_html}} />
  return <div className="text-sm leading-relaxed">{renderFormattedContent(body, isMe)}</div>
}

/**
 * Chat input area — text + file upload + send.
 */
export function ChatInputArea({ ws, ticketId, disabled }) {
  const [text, setText] = useState('')
  const { useState } = require('react')

  const send = e => {
    e.preventDefault()
    if (!text.trim() || !ws || disabled) return
    ws.send(JSON.stringify({ type:'message', body: text }))
    setText('')
  }

  return (
    <form onSubmit={send} className="flex gap-2">
      <input type="text" value={text} onChange={e => setText(e.target.value)}
        placeholder="Type a message…"
        className="flex-1 border border-[#E5E7F3] rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-indigo-400 outline-none"
        aria-label="Message input" />
      <button type="submit" disabled={!text.trim()||!ws}
        className="bg-[#6366F1] hover:bg-[#4F46E5] text-white px-5 rounded-xl transition-colors disabled:opacity-40 font-bold text-sm flex items-center gap-2 flex-shrink-0"
        aria-label="Send message">
        <Send size={16} /> Send
      </button>
    </form>
  )
}
