// Tailor Resume Page
'use client'
import { useEffect, useState } from 'react'
import axios from '@/lib/api'
import Navbar from '@/components/Navbar'

export default function TailorPage() {
  const [resumeFile, setResumeFile] = useState<File | null>(null)
  const [tailoredText, setTailoredText] = useState('')
  const [downloadLinks, setDownloadLinks] = useState<{ pdf: string; txt: string } | null>(null)
  const [status, setStatus] = useState('')
  const [preferences, setPreferences] = useState<any>(null)
  const [scrapedJob, setScrapedJob] = useState<any>(null)

  useEffect(() => {
    // Fetch saved preferences for this user
    const fetchPrefs = async () => {
      try {
        const res = await axios.get('/user/preferences')
        setPreferences(res.data)
      } catch (err) {
        console.error('Failed to load preferences', err)
      }
    }
    fetchPrefs()
  }, [])

  const handleScrapeJob = async () => {
    if (!preferences) return
    try {
      setStatus('Scraping Seek jobs...')
      const { job_title, location } = preferences
      const res = await axios.get(`/jobs/seek-jobs?job_title=${job_title}&location=${location}`)
      const topJob = res.data.jobs[0]
      setScrapedJob(topJob)
      setStatus(`Scraped: ${topJob.job_title} at ${topJob.company}`)
    } catch (err) {
      setStatus('Failed to scrape jobs')
    }
  }

  const handleTailor = async () => {
    if (!resumeFile || !scrapedJob) {
      setStatus('Upload a resume and scrape a job first.')
      return
    }
    setStatus('Uploading resume and tailoring...')
    const formData = new FormData()
    formData.append('file', resumeFile)
    try {
      // Upload + parse resume
      const uploadRes = await axios.post('/resume/upload-resume', formData)
      const parsedText = uploadRes.data.resume_text || ''

      // Tailor
      const tailorRes = await axios.post('/resume/generate-tailored-resume', {
        resume_text: parsedText,
        jd_text: scrapedJob.job_description,
        job_title: scrapedJob.job_title,
      })

      setTailoredText(tailorRes.data.tailored_resume_text)
      setDownloadLinks(tailorRes.data.files)
      setStatus('Resume tailored successfully')
    } catch (err: any) {
      console.error(err)
      setStatus('Tailoring failed: ' + (err.response?.data?.error || err.message))
    }
  }

  return (
    <div>
      <Navbar />
      <div className="p-6 max-w-3xl mx-auto">
        <h1 className="text-xl font-bold mb-4">Tailor Resume Automatically</h1>

        <input
          type="file"
          accept=".pdf,.doc,.docx"
          onChange={(e) => setResumeFile(e.target.files?.[0] || null)}
          className="mb-4"
        />

        <button onClick={handleScrapeJob} className="bg-blue-600 text-white px-4 py-2 rounded mr-2">
          Scrape Job
        </button>

        <button onClick={handleTailor} className="bg-green-600 text-white px-4 py-2 rounded">
          Tailor Resume
        </button>

        {status && <p className="mt-4 text-sm text-gray-700">{status}</p>}

        {tailoredText && (
          <div className="mt-6">
            <h2 className="font-bold text-lg mb-2">Tailored Resume</h2>
            <pre className="bg-gray-100 p-4 rounded whitespace-pre-wrap text-sm">
              {tailoredText}
            </pre>

            {downloadLinks && (
              <div className="mt-4 space-x-4">
                <a
                  href={downloadLinks.pdf}
                  className="bg-indigo-600 text-white px-4 py-2 rounded"
                  download
                >
                  Download PDF
                </a>
                <a
                  href={downloadLinks.txt}
                  className="bg-gray-600 text-white px-4 py-2 rounded"
                  download
                >
                  Download TXT
                </a>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

