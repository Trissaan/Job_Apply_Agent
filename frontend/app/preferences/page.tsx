// Preferences Page with Smart Suggestions (Dark Mode Fix)
'use client'
import { useEffect, useState } from 'react'
import axios from '@/lib/api'
import Navbar from '@/components/Navbar'

export default function PreferencesPage() {
  const [jobTitle, setJobTitle] = useState('')
  const [location, setLocation] = useState('')
  const [industry, setIndustry] = useState('')
  const [experience, setExperience] = useState('')
  const [status, setStatus] = useState('')
  const [jobSuggestions, setJobSuggestions] = useState<string[]>([])
  const [industryOptions, setIndustryOptions] = useState<string[]>([])

  useEffect(() => {
    const fetchPrefs = async () => {
      try {
        const res = await axios.get('/user/preferences')
        const prefs = res.data
        setJobTitle(prefs.job_title || '')
        setLocation(prefs.location || '')
        setIndustry(prefs.industry || '')
        setExperience(prefs.experience_level || '')
      } catch (err) {
        console.warn('No saved preferences found.')
      }
    }
    fetchPrefs()
  }, [])

  useEffect(() => {
    const loadSuggestions = async () => {
      if (jobTitle.length < 3) return
      try {
        const res = await axios.post('/user/suggest-job-titles', { query: jobTitle })
        setJobSuggestions(res.data.suggestions || [])
      } catch (err) {
        console.error('Failed to suggest job titles', err)
      }
    }
    loadSuggestions()
  }, [jobTitle])

  const handleTitleSelect = async (selected: string) => {
    setJobTitle(selected)
    try {
      const res = await axios.post('/user/suggest-industries', { job_title: selected })
      setIndustryOptions(res.data.industries || [])
    } catch (err) {
      console.error('Failed to fetch industries', err)
    }
  }

  const handleSave = async () => {
    try {
      await axios.post('/user/save-preferences', {
        job_title: jobTitle,
        location,
        industry,
        experience_level: experience,
      })
      setStatus('✅ Preferences saved successfully!')
    } catch (err) {
      console.error(err)
      setStatus('❌ Failed to save preferences')
    }
  }

  return (
    <div>
      <Navbar />
      <div className="p-6 max-w-xl mx-auto">
        <h1 className="text-xl font-bold mb-4">Job Preferences</h1>

        <input
          type="text"
          placeholder="Job Title"
          value={jobTitle}
          onChange={(e) => setJobTitle(e.target.value)}
          className="w-full p-2 mb-2 border rounded bg-white text-black"
        />
        {jobSuggestions.length > 0 && (
          <ul className="border bg-white text-black mb-3 rounded max-h-32 overflow-y-auto text-sm shadow">
            {jobSuggestions.map((suggestion, idx) => (
              <li
                key={idx}
                className="px-3 py-2 hover:bg-blue-100 cursor-pointer"
                onClick={() => handleTitleSelect(suggestion)}
              >
                {suggestion}
              </li>
            ))}
          </ul>
        )}

        <input
          type="text"
          placeholder="Location"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          className="w-full p-2 mb-3 border rounded bg-white text-black"
        />

        <select
          value={industry}
          onChange={(e) => setIndustry(e.target.value)}
          className="w-full p-2 mb-3 border rounded bg-white text-black"
        >
          <option value="">Select Industry</option>
          {industryOptions.map((opt, idx) => (
            <option key={idx} value={opt}>{opt}</option>
          ))}
        </select>

        <input
          type="text"
          placeholder="Experience Level (optional)"
          value={experience}
          onChange={(e) => setExperience(e.target.value)}
          className="w-full p-2 mb-4 border rounded bg-white text-black"
        />

        <button onClick={handleSave} className="bg-blue-600 text-white px-4 py-2 rounded">
          Save Preferences
        </button>

        {status && <p className="mt-4 text-sm">{status}</p>}
      </div>
    </div>
  )
}
