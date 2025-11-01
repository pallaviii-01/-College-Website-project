import { useEffect, useState } from 'react';
import Link from 'next/link';
import { isAuthenticated } from '@/utils/auth';

export default function Home() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    setIsLoggedIn(isAuthenticated());
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-primary-600">SkillPath Navigator</h1>
            </div>
            <div className="flex items-center space-x-4">
              {isLoggedIn ? (
                <Link href="/dashboard" className="btn-primary">
                  Dashboard
                </Link>
              ) : (
                <>
                  <Link href="/login" className="text-gray-700 hover:text-primary-600 font-medium">
                    Login
                  </Link>
                  <Link href="/register" className="btn-primary">
                    Get Started
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>

      <main>
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <h2 className="text-5xl font-bold text-gray-900 mb-6">
              Your Personalized Path to
              <span className="text-primary-600"> Skill Excellence</span>
            </h2>
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
              AI-powered learning recommendations aligned with NSQF standards. 
              Navigate your vocational training journey with personalized guidance 
              tailored to your goals and background.
            </p>
            <div className="flex justify-center space-x-4">
              <Link href="/register" className="btn-primary text-lg px-8 py-4">
                Start Your Journey
              </Link>
              <Link href="/about" className="btn-secondary text-lg px-8 py-4">
                Learn More
              </Link>
            </div>
          </div>
        </section>

        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <h3 className="text-3xl font-bold text-center text-gray-900 mb-12">
            How It Works
          </h3>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="card text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-3xl font-bold text-primary-600">1</span>
              </div>
              <h4 className="text-xl font-semibold mb-3">Create Your Profile</h4>
              <p className="text-gray-600">
                Tell us about your education, skills, and career aspirations. 
                Our AI analyzes your unique background.
              </p>
            </div>

            <div className="card text-center">
              <div className="w-16 h-16 bg-secondary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-3xl font-bold text-secondary-600">2</span>
              </div>
              <h4 className="text-xl font-semibold mb-3">Get Recommendations</h4>
              <p className="text-gray-600">
                Receive personalized course recommendations mapped to NSQF levels 
                and aligned with industry demands.
              </p>
            </div>

            <div className="card text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-3xl font-bold text-primary-600">3</span>
              </div>
              <h4 className="text-xl font-semibold mb-3">Track Progress</h4>
              <p className="text-gray-600">
                Follow your customized learning path and watch your skills grow. 
                Adapt as you progress and market trends evolve.
              </p>
            </div>
          </div>
        </section>

        <section className="bg-primary-600 text-white py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid md:grid-cols-2 gap-12 items-center">
              <div>
                <h3 className="text-3xl font-bold mb-6">
                  Powered by AI, Aligned with NSQF
                </h3>
                <ul className="space-y-4">
                  <li className="flex items-start">
                    <span className="text-secondary-400 mr-3 text-xl">✓</span>
                    <span>Personalized recommendations based on your unique profile</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-secondary-400 mr-3 text-xl">✓</span>
                    <span>Real-time labor market intelligence integration</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-secondary-400 mr-3 text-xl">✓</span>
                    <span>NSQF-aligned qualifications and certifications</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-secondary-400 mr-3 text-xl">✓</span>
                    <span>Multilingual support for diverse learners</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-secondary-400 mr-3 text-xl">✓</span>
                    <span>Adaptive pathways that evolve with your progress</span>
                  </li>
                </ul>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8">
                <h4 className="text-2xl font-bold mb-4">Ready to Begin?</h4>
                <p className="mb-6">
                  Join thousands of learners who are building future-ready skills 
                  with personalized guidance.
                </p>
                <Link href="/register" className="inline-block bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
                  Create Free Account
                </Link>
              </div>
            </div>
          </div>
        </section>

        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <h3 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Key Features
          </h3>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="card">
              <h4 className="font-semibold text-lg mb-2">Smart Profiling</h4>
              <p className="text-gray-600 text-sm">
                Comprehensive learner assessment considering education, skills, and aspirations
              </p>
            </div>
            <div className="card">
              <h4 className="font-semibold text-lg mb-2">Career Pathways</h4>
              <p className="text-gray-600 text-sm">
                Sequential learning paths designed to achieve your career goals
              </p>
            </div>
            <div className="card">
              <h4 className="font-semibold text-lg mb-2">Skill Gap Analysis</h4>
              <p className="text-gray-600 text-sm">
                Identify missing skills and get targeted recommendations
              </p>
            </div>
            <div className="card">
              <h4 className="font-semibold text-lg mb-2">Market Insights</h4>
              <p className="text-gray-600 text-sm">
                Real-time job market data to guide your learning decisions
              </p>
            </div>
          </div>
        </section>
      </main>

      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-3 gap-8">
            <div>
              <h5 className="text-xl font-bold mb-4">SkillPath Navigator</h5>
              <p className="text-gray-400">
                Empowering learners with AI-driven personalized vocational training pathways.
              </p>
            </div>
            <div>
              <h6 className="font-semibold mb-4">Quick Links</h6>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/about" className="hover:text-white">About Us</Link></li>
                <li><Link href="/courses" className="hover:text-white">Browse Courses</Link></li>
                <li><Link href="/contact" className="hover:text-white">Contact</Link></li>
              </ul>
            </div>
            <div>
              <h6 className="font-semibold mb-4">Powered By</h6>
              <p className="text-gray-400">
                National Council for Vocational Education and Training (NCVET)
              </p>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2025 SkillPath Navigator. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
