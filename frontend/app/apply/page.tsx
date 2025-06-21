'use client'
import Navbar from '@/components/Navbar'
import { useState } from 'react'
import axios from '@/lib/api'

export default function AutoApplyPage() {
  const [status, setStatus] = useState('')

  const handleApply = async () => {
    setStatus('Running job scraper and auto-apply...')
    try {
      await axios.get('/jobs/seek-jobs?job_title=data analyst&location=melbourne')
      setStatus('Jobs scraped. Agent is applying...')
      // TODO: Trigger runner or apply endpoint if exposed
    } catch (err: any) {
      setStatus('Failed to trigger job agent')
    }
  }

  return (
    <div>
      <Navbar />
      <div className="p-6 max-w-xl mx-auto">
        <h1 className="text-xl font-bold mb-4">AI Auto Apply</h1>
        <button className="bg-green-600 text-white px-4 py-2 rounded" onClick={handleApply}>
          Run Auto Apply Bot
        </button>
        <p className="mt-4 text-sm">{status}</p>
      </div>
    </div>
  )
}
