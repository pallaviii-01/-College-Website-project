import { useState } from 'react';
import { apiClient } from '@/utils/api';

interface OnboardingWizardProps {
  onComplete: () => void;
}

const SKILLS_OPTIONS = [
  'Python', 'Java', 'JavaScript', 'Data Analysis', 'Machine Learning',
  'SQL', 'Communication', 'Leadership', 'Project Management', 'Excel',
  'Digital Marketing', 'Graphic Design', 'Accounting', 'Customer Service',
  'Sales', 'Content Writing', 'Web Development', 'Mobile Development'
];

const CAREER_OPTIONS = [
  'Data Scientist', 'Software Engineer', 'Web Developer', 'Digital Marketer',
  'Business Analyst', 'Project Manager', 'Graphic Designer', 'Accountant',
  'Sales Manager', 'HR Professional', 'Content Writer', 'Teacher'
];

export default function OnboardingWizard({ onComplete }: OnboardingWizardProps) {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const [profileData, setProfileData] = useState({
    education_level: 'graduate',
    prior_skills: [] as string[],
    career_aspirations: [] as string[],
    socio_economic_status: 'middle_class',
    learning_pace: 'moderate',
    location: '',
    age: 25,
    work_experience_years: 0,
    current_occupation: '',
    interests: [] as string[],
    constraints: {},
  });

  const handleSkillToggle = (skill: string) => {
    setProfileData(prev => ({
      ...prev,
      prior_skills: prev.prior_skills.includes(skill)
        ? prev.prior_skills.filter(s => s !== skill)
        : [...prev.prior_skills, skill]
    }));
  };

  const handleCareerToggle = (career: string) => {
    setProfileData(prev => ({
      ...prev,
      career_aspirations: prev.career_aspirations.includes(career)
        ? prev.career_aspirations.filter(c => c !== career)
        : [...prev.career_aspirations, career]
    }));
  };

  const handleInterestToggle = (interest: string) => {
    setProfileData(prev => ({
      ...prev,
      interests: prev.interests.includes(interest)
        ? prev.interests.filter(i => i !== interest)
        : [...prev.interests, interest]
    }));
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError('');

    try {
      await apiClient.createLearnerProfile({
        ...profileData,
        user_id: 0,
      });
      onComplete();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create profile');
    } finally {
      setLoading(false);
    }
  };

  const nextStep = () => {
    if (step < 4) setStep(step + 1);
  };

  const prevStep = () => {
    if (step > 1) setStep(step - 1);
  };

  return (
    <div className="max-w-3xl mx-auto">
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          {[1, 2, 3, 4].map((s) => (
            <div key={s} className="flex items-center flex-1">
              <div
                className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold ${
                  s <= step
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-200 text-gray-600'
                }`}
              >
                {s}
              </div>
              {s < 4 && (
                <div
                  className={`flex-1 h-1 mx-2 ${
                    s < step ? 'bg-primary-600' : 'bg-gray-200'
                  }`}
                />
              )}
            </div>
          ))}
        </div>
        <div className="flex justify-between text-sm text-gray-600">
          <span>Basic Info</span>
          <span>Skills</span>
          <span>Career Goals</span>
          <span>Preferences</span>
        </div>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg">
          {error}
        </div>
      )}

      <div className="bg-white rounded-xl shadow-lg p-8">
        {step === 1 && (
          <div className="space-y-6">
            <h3 className="text-2xl font-bold text-gray-900 mb-6">Basic Information</h3>
            
            <div>
              <label className="label">Education Level</label>
              <select
                value={profileData.education_level}
                onChange={(e) => setProfileData({ ...profileData, education_level: e.target.value })}
                className="input-field"
              >
                <option value="below_10th">Below 10th</option>
                <option value="10th">10th Standard</option>
                <option value="12th">12th Standard</option>
                <option value="diploma">Diploma</option>
                <option value="graduate">Graduate</option>
                <option value="post_graduate">Post Graduate</option>
                <option value="doctorate">Doctorate</option>
              </select>
            </div>

            <div>
              <label className="label">Age</label>
              <input
                type="number"
                min="15"
                max="100"
                value={profileData.age}
                onChange={(e) => setProfileData({ ...profileData, age: parseInt(e.target.value) })}
                className="input-field"
              />
            </div>

            <div>
              <label className="label">Work Experience (Years)</label>
              <input
                type="number"
                min="0"
                max="50"
                value={profileData.work_experience_years}
                onChange={(e) => setProfileData({ ...profileData, work_experience_years: parseInt(e.target.value) })}
                className="input-field"
              />
            </div>

            <div>
              <label className="label">Current Occupation (Optional)</label>
              <input
                type="text"
                value={profileData.current_occupation}
                onChange={(e) => setProfileData({ ...profileData, current_occupation: e.target.value })}
                className="input-field"
                placeholder="e.g., Student, Sales Executive, etc."
              />
            </div>

            <div>
              <label className="label">Location</label>
              <input
                type="text"
                value={profileData.location}
                onChange={(e) => setProfileData({ ...profileData, location: e.target.value })}
                className="input-field"
                placeholder="City, State"
              />
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="space-y-6">
            <h3 className="text-2xl font-bold text-gray-900 mb-6">Your Skills</h3>
            <p className="text-gray-600 mb-4">Select all skills you currently have</p>
            
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {SKILLS_OPTIONS.map((skill) => (
                <button
                  key={skill}
                  type="button"
                  onClick={() => handleSkillToggle(skill)}
                  className={`p-3 rounded-lg border-2 text-sm font-medium transition-colors ${
                    profileData.prior_skills.includes(skill)
                      ? 'border-primary-600 bg-primary-50 text-primary-700'
                      : 'border-gray-200 bg-white text-gray-700 hover:border-primary-300'
                  }`}
                >
                  {skill}
                </button>
              ))}
            </div>
          </div>
        )}

        {step === 3 && (
          <div className="space-y-6">
            <h3 className="text-2xl font-bold text-gray-900 mb-6">Career Aspirations</h3>
            <p className="text-gray-600 mb-4">What career paths interest you?</p>
            
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {CAREER_OPTIONS.map((career) => (
                <button
                  key={career}
                  type="button"
                  onClick={() => handleCareerToggle(career)}
                  className={`p-3 rounded-lg border-2 text-sm font-medium transition-colors ${
                    profileData.career_aspirations.includes(career)
                      ? 'border-secondary-600 bg-secondary-50 text-secondary-700'
                      : 'border-gray-200 bg-white text-gray-700 hover:border-secondary-300'
                  }`}
                >
                  {career}
                </button>
              ))}
            </div>
          </div>
        )}

        {step === 4 && (
          <div className="space-y-6">
            <h3 className="text-2xl font-bold text-gray-900 mb-6">Learning Preferences</h3>
            
            <div>
              <label className="label">Learning Pace</label>
              <select
                value={profileData.learning_pace}
                onChange={(e) => setProfileData({ ...profileData, learning_pace: e.target.value })}
                className="input-field"
              >
                <option value="slow">Slow - I prefer to take my time</option>
                <option value="moderate">Moderate - Balanced approach</option>
                <option value="fast">Fast - I learn quickly</option>
              </select>
            </div>

            <div>
              <label className="label">Socio-Economic Status</label>
              <select
                value={profileData.socio_economic_status}
                onChange={(e) => setProfileData({ ...profileData, socio_economic_status: e.target.value })}
                className="input-field"
              >
                <option value="bpl">Below Poverty Line</option>
                <option value="apl">Above Poverty Line</option>
                <option value="middle_class">Middle Class</option>
                <option value="upper_middle">Upper Middle Class</option>
              </select>
            </div>

            <div>
              <label className="label mb-3">Areas of Interest</label>
              <div className="grid grid-cols-2 gap-3">
                {['Technology', 'Business', 'Healthcare', 'Education', 'Arts', 'Manufacturing'].map((interest) => (
                  <button
                    key={interest}
                    type="button"
                    onClick={() => handleInterestToggle(interest)}
                    className={`p-3 rounded-lg border-2 text-sm font-medium transition-colors ${
                      profileData.interests.includes(interest)
                        ? 'border-primary-600 bg-primary-50 text-primary-700'
                        : 'border-gray-200 bg-white text-gray-700 hover:border-primary-300'
                    }`}
                  >
                    {interest}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        <div className="flex justify-between mt-8 pt-6 border-t">
          <button
            onClick={prevStep}
            disabled={step === 1}
            className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          
          {step < 4 ? (
            <button onClick={nextStep} className="btn-primary">
              Next
            </button>
          ) : (
            <button
              onClick={handleSubmit}
              disabled={loading}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Creating Profile...' : 'Complete Setup'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
