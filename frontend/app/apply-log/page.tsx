'use client'
import { useEffect, useState } from 'react'
import Navbar from '@/components/Navbar'

interface LogEntry {
  job_title: string
  company: string
  platform: string
  job_url: string
  status: string
  timestamp: string
  tags: string[]
}

export default function ApplyLogPage() {
  const [logs, setLogs] = useState<LogEntry[]>([])

  useEffect(() => {
    fetch('http://localhost:8000/static/applications.json')
      .then((res) => res.json())
      .then(setLogs)
      .catch(console.error)
  }, [])

  return (
    <div>
      <Navbar />
      <div className="p-6 max-w-4xl mx-auto">
        <h1 className="text-xl font-bold mb-4">Applied Jobs</h1>
        <ul className="space-y-4">
          {logs.map((log, i) => (
            <li key={i} className="border p-4 rounded">
              <h2 className="font-semibold">{log.job_title} at {log.company}</h2>
              <p className="text-sm text-gray-500">{log.platform} | {new Date(log.timestamp).toLocaleString()}</p>
              <p>Status: {log.status}</p>
              <a href={log.job_url} className="text-blue-600 underline text-sm" target="_blank">View Job</a>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
