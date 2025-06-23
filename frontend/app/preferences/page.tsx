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

  const handleSave = async () => {
    try {
      await axios.post('/user/save-preferences', {
        job_title: jobTitle,
        location,
        industry,
        experience_level: experience,
      })
      setStatus(' Preferences saved successfully!')
    } catch (err) {
      console.error(err)
      setStatus(' Failed to save preferences')
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
          className="w-full p-2 mb-3 border rounded"
        />

        <input
          type="text"
          placeholder="Location"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          className="w-full p-2 mb-3 border rounded"
        />

        <input
          type="text"
          placeholder="Industry (optional)"
          value={industry}
          onChange={(e) => setIndustry(e.target.value)}
          className="w-full p-2 mb-3 border rounded"
        />

        <input
          type="text"
          placeholder="Experience Level (optional)"
          value={experience}
          onChange={(e) => setExperience(e.target.value)}
          className="w-full p-2 mb-4 border rounded"
        />

        <button onClick={handleSave} className="bg-blue-600 text-white px-4 py-2 rounded">
          Save Preferences
        </button>

        {status && <p className="mt-4 text-sm">{status}</p>}
      </div>
    </div>
  )
}