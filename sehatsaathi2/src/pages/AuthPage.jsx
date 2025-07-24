import React, { useState,useEffect } from 'react';
import styles from '../styles/Auth.module.css';
import axios from 'axios';
import { useNavigate, useLocation} from 'react-router-dom';

const AuthSite = () => {

  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const defaultTab = searchParams.get('tab') || 'signup'; 
  const [activeTab, setActiveTab] = useState(defaultTab);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });

  useEffect(() => {
    setActiveTab(defaultTab);
  }, [defaultTab]);


  const [message, setMessage] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const navigate = useNavigate();

  const isPasswordStrong = (password) => {
    const strongPasswordRegex =
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    return strongPasswordRegex.test(password);
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (event, type) => {
    event.preventDefault();
    setErrorMessage('');
    setPasswordError('');

    if (type === 'signup') {
      if (!isPasswordStrong(formData.password)) {
        setPasswordError(
          'Password must have at least 8 characters, one uppercase, one lowercase, one number, and one special character.'
        );
        return;
      }

      if (formData.password !== formData.confirmPassword) {
        setPasswordError('Passwords do not match');
        return;
      }

       // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      setErrorMessage('Please enter a valid email address.');
      return;
    }

    
      try {
        const res = await axios.post('http://localhost:3001/api/auth/signup', {
          name: formData.name,
          email: formData.email,
          password: formData.password,
        });

        console.log('Signup successful', res);
        setFormData({ name: '', email: '', password: '', confirmPassword: '' });

        navigate('/auth?tab=signin');
        setMessage('Account created successfully. You can now sign in.');
      } catch (err) {
        console.error('Signup error', err);
        setErrorMessage(err.response?.data?.message || 'Signup failed. Please try again.');
      }
    } else {
      try {
        const res = await axios.post('http://localhost:3001/api/auth/signin', {
          email: formData.email,
          password: formData.password,
        });

        if (res.data.token) {
          localStorage.setItem('token', res.data.token);
          console.log('Login successful', res);
          setMessage('Login successful');
          navigate('/dashboard');
        } else {
          setErrorMessage('Invalid login response. Please try again.');
        }
      } catch (err) {
        console.error('Login error', err);
        setErrorMessage(err.response?.data?.message || 'Login failed. Please try again.');
      }
    }
  };

  return (
    <div className={styles.authContainer}>
      <div className={styles.authCard}>
        <h1 className={styles.title}>
          {activeTab === 'signin' ? 'Welcome Back' : 'Create an Account'}
        </h1>

        <div className={styles.tabs}>
          <div
            className={`${styles.tab} ${activeTab === 'signin' ? styles.active : ''}`}
            onClick={() =>{ navigate('/auth?tab=signin')
              setFormData({ name: '', email: '', password: '', confirmPassword: '' });
            }}
          >
            Sign In
          </div>
          <div
            className={`${styles.tab} ${activeTab === 'signup' ? styles.active : ''}`}
            onClick={() => {navigate('/auth?tab=signup')

            }}
          >
            Sign Up
          </div>
        </div>

        {activeTab === 'signin' ? (
          <form onSubmit={(e) => handleSubmit(e, 'signin')}>
            <div className={styles.formGroup}>
              <label>Email</label>
              <input
                type="email"
                name="email"
                placeholder="you@example.com"
                value={formData.email}
                onChange={handleChange}
                required
                className={styles.input}
              />
            </div>

            <div className={styles.formGroup}>
              <label>Password</label>
              <input
                type="password"
                name="password"
                placeholder="••••••••"
                value={formData.password}
                onChange={handleChange}
                required
                className={styles.input}
              />
            </div>

            {errorMessage && <p className={styles.errorMessage}>{errorMessage}</p>}
            {message && <p className={styles.success}>{message}</p>}

            <button type="submit" className={styles.btn}>Sign In</button>
          </form>
        ) : (
          <form onSubmit={(e) => handleSubmit(e, 'signup')}>
            <div className={styles.formGroup}>
              <label>Full Name</label>
              <input
                type="text"
                name="name"
                placeholder="Your Name"
                value={formData.name}
                onChange={handleChange}
                required
                className={styles.input}
              />
            </div>

            <div className={styles.formGroup}>
              <label>Email</label>
              <input
                type="email"
                name="email"
                placeholder="you@example.com"
                value={formData.email}
                onChange={handleChange}
                required
                className={styles.input}
              />
            </div>

            <div className={styles.formGroup}>
              <label>Password</label>
              <input
                type="password"
                name="password"
                placeholder="••••••••"
                value={formData.password}
                onChange={handleChange}
                required
                className={styles.input}
              />
            </div>

            <div className={styles.formGroup}>
              <label>Confirm Password</label>
              <input
                type="password"
                name="confirmPassword"
                placeholder="••••••••"
                value={formData.confirmPassword}
                onChange={handleChange}
                required
                className={styles.input}
              />
            </div>

            {passwordError && <p className={styles.passwordError}>{passwordError}</p>}
            {errorMessage && <p className={styles.errorMessage}>{errorMessage}</p>}
            {message && <p className={styles.success}>{message}</p>}

            <button type="submit" className={styles.btn}>Create Account</button>
          </form>
        )}


<p className={styles.footerText}>
          {activeTab === 'signin' ? (
            <>Don't have an account? <a href="#" onClick={() => setActiveTab('signup')} className={styles.link}>Sign up</a></>
          ) : (
            <>Already have an account? <a href="#" onClick={() => setActiveTab('signin')} className={styles.link}>Sign in</a></>
          )}
        </p>
      </div>
    </div>
  );
};

export default AuthSite;
