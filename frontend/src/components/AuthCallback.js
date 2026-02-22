import { useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { authAPI } from '@/utils/api';

const AuthCallback = () => {
  const navigate = useNavigate();
  const { setUser, setIsAuthenticated } = useAuth();
  const hasProcessed = useRef(false);

  useEffect(() => {
    // Prevent double processing in StrictMode
    if (hasProcessed.current) return;
    hasProcessed.current = true;

    const processCallback = async () => {
      console.log('=== AuthCallback Processing ===');
      const hash = window.location.hash;
      console.log('URL hash:', hash);
      
      const params = new URLSearchParams(hash.substring(1));
      const sessionId = params.get('session_id');
      console.log('Session ID:', sessionId);

      if (!sessionId) {
        console.error('No session_id found in URL');
        navigate('/');
        return;
      }

      try {
        console.log('Calling /api/auth/session...');
        const response = await authAPI.exchangeSession(sessionId);
        console.log('Session exchange response:', response.data);
        
        const userData = response.data.user;
        console.log('User data:', userData);
        
        setUser(userData);
        setIsAuthenticated(true);
        
        console.log('Auth state updated, navigating to dashboard...');
        
        // Small delay to ensure state is set
        setTimeout(() => {
          navigate('/dashboard', { state: { user: userData }, replace: true });
        }, 100);
        
      } catch (error) {
        console.error('Auth callback error:', error);
        console.error('Error details:', error.response?.data);
        navigate('/', { replace: true });
      }
    };

    processCallback();
  }, [navigate, setUser, setIsAuthenticated]);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Completing sign in...</p>
        <p className="mt-2 text-sm text-gray-500">Please wait</p>
      </div>
    </div>
  );
};

export default AuthCallback;
