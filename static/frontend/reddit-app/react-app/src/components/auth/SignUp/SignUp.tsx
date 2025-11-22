import React, { useState } from 'react';
import './SignUp.scss';

const SignUp = () => {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [hidePassword, setHidePassword] = useState(true);

  const toggleVisibility = () => {
    setHidePassword(!hidePassword);
  };

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      alert("Passwords don't match");
      return;
    }
    const signUpData = {
      first_name: firstName,
      last_name: lastName,
      email,
      password,
    };
    setIsLoading(true);
    // Placeholder for userService.register
    console.log('Signing up with:', signUpData);
    setTimeout(() => {
      setIsLoading(false);
      // Placeholder for snackbar
      alert('Successfully signed up');
      // router.navigate(['/sign-in']);
    }, 1000);
  };

  return (
    <div className="auth-container">
      <div className="login-form">
        <h2 className="text-white" style={{ textAlign: 'center' }}>Sign up for Django-Reddit</h2>

        <form className="width-100 auth-form" autoComplete="off" onSubmit={onSubmit}>
          <div className="input-column" style={{ display: 'flex', gap: '16px' }}>
            <div className="width-100 margin-bottom-4">
              <label htmlFor="firstname">First name</label>
              <input
                id="firstname"
                placeholder="John"
                type="text"
                className="form-input"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                required
              />
            </div>

            <div className="width-100 margin-bottom-4">
              <label htmlFor="lastname">Last name</label>
              <input
                id="lastname"
                placeholder="Doe"
                type="text"
                className="form-input"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="width-100 margin-bottom-4">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              placeholder="jane@email.com"
              type="email"
              className="form-input"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="input-column margin-bottom-4" style={{ display: 'flex', gap: '16px', position: 'relative' }}>
            <div className="width-100">
              <label htmlFor="password">Password</label>
              <input
                id="password"
                placeholder="dankworld12"
                type={hidePassword ? 'password' : 'text'}
                className="form-input"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <button type="button" className="toggle-visibility-btn" onClick={toggleVisibility} aria-label="Hide password" aria-pressed={hidePassword}>
                {hidePassword ? 'visibility_off' : 'visibility'}
              </button>
            </div>

            <div className="width-100">
              <label htmlFor="confirmPassword">Confirm password</label>
              <input
                id="confirmPassword"
                placeholder="dankworld12"
                type={hidePassword ? 'password' : 'text'}
                className="form-input"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
              />
              <button type="button" className="toggle-visibility-btn" onClick={toggleVisibility} aria-label="Hide password" aria-pressed={hidePassword}>
                {hidePassword ? 'visibility_off' : 'visibility'}
              </button>
            </div>
          </div>

          <button
            type="submit"
            className="width-100 custom-button block-button"
            disabled={!firstName || !lastName || !email || !password || !confirmPassword || isLoading}
          >
            {isLoading ? 'Loading...' : 'Submit'}
          </button>

          <p>Already have an account? <a className="underline button-link" href="../sign-in">Sign In</a></p>
        </form>.
      </div>
    </div>
  );
};

export default SignUp;
