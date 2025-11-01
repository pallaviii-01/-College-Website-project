import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { isAuthenticated } from '@/utils/auth';
import OnboardingWizard from '@/components/OnboardingWizard';

export default function Onboarding() {
  const router = useRouter();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    if (!isAuthenticated()) {
      router.push('/login');
    }
  }, [router]);

  const handleComplete = () => {
    router.push('/dashboard');
  };

  if (!mounted) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Let's Build Your Learning Profile
          </h1>
          <p className="text-xl text-gray-600">
            Help us understand your background and goals to provide personalized recommendations
          </p>
        </div>

        <OnboardingWizard onComplete={handleComplete} />
      </div>
    </div>
  );
}
