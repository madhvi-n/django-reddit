import React, { useState } from 'react';
import './SignIn.scss';

const SignIn = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [hidePassword, setHidePassword] = useState(true);

  const toggleVisibility = () => {
    setHidePassword(!hidePassword);
  };

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const loginData = {
      email,
      password
    };
    setIsLoading(true);
    // Placeholder for userService.login
    console.log('Logging in with:', loginData);
    setTimeout(() => {
      setIsLoading(false);
      // Placeholder for snackbar
      alert('Successfully logged in');
      // router.navigate(['']);
    }, 1000);
  };

  return (
    <div className="auth-container">
      <div className="login-form">
        <h2 className="text-white" style={{ textAlign: 'center' }}>Sign in to Django Reddit</h2>

        <div className="buttons-section">
          <button className="custom-button" disabled style={{ borderColor: 'rgb(255, 92, 136)' }}>Google</button>
          <button className="custom-button" disabled style={{ borderColor: 'rgb(255, 192, 93)' }}>Facebook</button>
        </div>

        <div className="separator-section">
          <div className="divider-left"></div>
          <p style={{ textAlign: 'center' }}>OR</p>
          <div className="divider-right"></div>
        </div>

        <form className="width-100 auth-form" autoComplete="off" onSubmit={onSubmit}>
          <div className="width-100 margin-bottom-4">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              placeholder="jane@email.com"
              type="email"
              className="form-input"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div className="width-100 margin-bottom-4" style={{ position: 'relative' }}>
            <label htmlFor="password">Password</label>
            <input
              id="password"
              placeholder="wonderfullemon dankworld"
              type={hidePassword ? 'password' : 'text'}
              className="form-input"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <button type="button" className="toggle-visibility-btn" onClick={toggleVisibility} aria-label="Hide password" aria-pressed={hidePassword}>
              {hidePassword ? 'visibility_off' : 'visibility'}
            </button>
          </div>

          <button type="submit" className="margin-top-4 width-100 custom-button block-button submit-button" disabled={!email || !password || isLoading}>
            {isLoading ? 'Loading...' : 'Submit'}
          </button>

          <p>Haven't registered yet? <a className="underline button-link" href="../sign-up">Sign Up</a></p>
        </form>
      </div>
    </div>
  );
};

export default SignIn;
