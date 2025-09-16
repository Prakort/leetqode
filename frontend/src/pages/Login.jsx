import React, { useEffect } from 'react';
import { Code } from 'lucide-react';
import useAuthStore from '../store/authStore';

const Login = () => {
  const { login } = useAuthStore();

  useEffect(() => {
    // Load Google Identity Services
    const loadGoogleScript = () => {
      return new Promise((resolve, reject) => {
        if (window.google?.accounts) {
          resolve();
          return;
        }
        
        const script = document.createElement('script');
        script.src = 'https://accounts.google.com/gsi/client';
        script.async = true;
        script.defer = true;
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
      });
    };

    const initGoogleSignIn = async () => {
      try {
        await loadGoogleScript();
        
        // Wait for Google Identity Services to be available
        const checkGoogle = setInterval(() => {
          if (window.google?.accounts) {
            clearInterval(checkGoogle);
            
            // Initialize Google Identity Services
            window.google.accounts.id.initialize({
              client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID || '283307083033-qh48bj9liq495l3ge5s843s4uhm7q07j.apps.googleusercontent.com',
              callback: onSignIn,
              auto_select: false,
              cancel_on_tap_outside: true,
            });
          }
        }, 100);
        
      } catch (error) {
        console.error('Failed to load Google Identity Services:', error);
      }
    };

    initGoogleSignIn();
  }, []);

  const onSignIn = (response) => {
    console.log('Google Sign-In successful:', response);
    
    // Send the credential (JWT token) to backend for verification
    login(response.credential);
  };

  // Make onSignIn globally available for Google Identity Services
  useEffect(() => {
    window.onSignIn = onSignIn;
    return () => {
      delete window.onSignIn;
    };
  }, [onSignIn]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <div className="flex justify-center">
            <div className="w-16 h-16 bg-primary-600 rounded-2xl flex items-center justify-center">
              <Code className="w-8 h-8 text-white" />
            </div>
          </div>
          <h2 className="mt-6 text-3xl font-extrabold text-gray-900">
            Welcome to LeetQode
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Track your LeetCode practice with confidence-based spaced repetition
          </p>
        </div>
        
        <div className="mt-8 space-y-6">
          <div className="bg-white p-8 rounded-lg shadow-md">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              Sign in to continue
            </h3>
            <p className="text-sm text-gray-600 mb-6">
              Use your Google account to sign in and start tracking your coding practice.
            </p>
            
            {/* Google Sign-In Button */}
            <div id="g_id_onload"
                 data-client_id={import.meta.env.VITE_GOOGLE_CLIENT_ID || '283307083033-qh48bj9liq495l3ge5s843s4uhm7q07j.apps.googleusercontent.com'}
                 data-callback="onSignIn"
                 data-auto_prompt="false">
            </div>
            <div className="g_id_signin"
                 data-type="standard"
                 data-size="large"
                 data-theme="outline"
                 data-text="sign_in_with"
                 data-shape="rectangular"
                 data-logo_alignment="left">
            </div>
          </div>
          
          <div className="text-center">
            <p className="text-xs text-gray-500">
              By signing in, you agree to our terms of service and privacy policy.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
