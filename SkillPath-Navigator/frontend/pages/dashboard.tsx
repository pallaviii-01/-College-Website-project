import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { isAuthenticated } from '@/utils/auth';
import { apiClient } from '@/utils/api';

export default function Dashboard() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [profile, setProfile] = useState<any>(null);
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push('/login');
      return;
    }

    loadDashboardData();
  }, [router]);

  const loadDashboardData = async () => {
    try {
      const [userData, profileData, recsData] = await Promise.all([
        apiClient.getCurrentUser(),
        apiClient.getLearnerProfile().catch(() => null),
        apiClient.getRecommendations({ top_k: 6 }).catch(() => ({ recommendations: [] })),
      ]);

      setUser(userData);
      setProfile(profileData);
      setRecommendations(recsData.recommendations || []);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    apiClient.logout();
    router.push('/');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="max-w-md text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Complete Your Profile</h2>
          <p className="text-gray-600 mb-6">
            Please complete your learner profile to get personalized recommendations.
          </p>
          <Link href="/onboarding" className="btn-primary">
            Complete Profile
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link href="/" className="text-2xl font-bold text-primary-600">
              SkillPath Navigator
            </Link>
            <div className="flex items-center space-x-6">
              <Link href="/dashboard" className="text-gray-700 hover:text-primary-600 font-medium">
                Dashboard
              </Link>
              <Link href="/courses" className="text-gray-700 hover:text-primary-600 font-medium">
                Courses
              </Link>
              <Link href="/learning-path" className="text-gray-700 hover:text-primary-600 font-medium">
                Learning Path
              </Link>
              <button
                onClick={handleLogout}
                className="text-gray-700 hover:text-primary-600 font-medium"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome back, {user?.full_name}!
          </h1>
          <p className="text-gray-600 mt-2">
            Continue your personalized learning journey
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <div className="card">
            <h3 className="text-sm font-medium text-gray-600 mb-2">Current Skills</h3>
            <p className="text-3xl font-bold text-primary-600">
              {profile?.prior_skills?.length || 0}
            </p>
          </div>
          <div className="card">
            <h3 className="text-sm font-medium text-gray-600 mb-2">Career Goals</h3>
            <p className="text-3xl font-bold text-secondary-600">
              {profile?.career_aspirations?.length || 0}
            </p>
          </div>
          <div className="card">
            <h3 className="text-sm font-medium text-gray-600 mb-2">Education Level</h3>
            <p className="text-xl font-bold text-gray-900 capitalize">
              {profile?.education_level?.replace('_', ' ')}
            </p>
          </div>
        </div>

        <div className="mb-8">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">
              Recommended Courses for You
            </h2>
            <Link href="/recommendations" className="text-primary-600 hover:text-primary-700 font-medium">
              View All →
            </Link>
          </div>

          {recommendations.length > 0 ? (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {recommendations.map((rec: any) => (
                <div key={rec.course_id} className="card">
                  <div className="flex items-start justify-between mb-3">
                    <span className="px-3 py-1 bg-primary-100 text-primary-700 text-xs font-semibold rounded-full">
                      NSQF Level {rec.nsqf_level}
                    </span>
                    <span className="text-sm font-semibold text-secondary-600">
                      {Math.round(rec.relevance_score * 100)}% Match
                    </span>
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    {rec.course_title}
                  </h3>
                  <p className="text-sm text-gray-600 mb-3">
                    {rec.sector}
                  </p>
                  {rec.explanation && (
                    <p className="text-sm text-gray-500 mb-4 line-clamp-2">
                      {rec.explanation}
                    </p>
                  )}
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-500">
                      {rec.estimated_duration_hours}h
                    </span>
                    <Link
                      href={`/courses/${rec.course_id}`}
                      className="text-primary-600 hover:text-primary-700 font-medium text-sm"
                    >
                      View Details →
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="card text-center py-12">
              <p className="text-gray-600 mb-4">
                No recommendations available yet. Complete your profile to get personalized suggestions.
              </p>
              <Link href="/onboarding" className="btn-primary">
                Update Profile
              </Link>
            </div>
          )}
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div className="card">
            <h3 className="text-xl font-bold text-gray-900 mb-4">Your Skills</h3>
            <div className="flex flex-wrap gap-2">
              {profile?.prior_skills?.map((skill: string) => (
                <span
                  key={skill}
                  className="px-3 py-1 bg-primary-50 text-primary-700 text-sm rounded-full"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>

          <div className="card">
            <h3 className="text-xl font-bold text-gray-900 mb-4">Career Aspirations</h3>
            <div className="flex flex-wrap gap-2">
              {profile?.career_aspirations?.map((career: string) => (
                <span
                  key={career}
                  className="px-3 py-1 bg-secondary-50 text-secondary-700 text-sm rounded-full"
                >
                  {career}
                </span>
              ))}
            </div>
          </div>
        </div>

        <div className="mt-8 card bg-gradient-to-r from-primary-600 to-secondary-600 text-white">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-xl font-bold mb-2">Generate Your Learning Path</h3>
              <p className="text-primary-100">
                Get a personalized, sequential learning roadmap to achieve your career goals
              </p>
            </div>
            <Link href="/learning-path" className="bg-white text-primary-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
              Create Path
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
}
