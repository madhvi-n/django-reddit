import React, { useEffect, useState } from 'react';
import './SignOut.scss';

const SignOut = () => {
  const [context, setContext] = useState({ title: '', subtitle: '' });
  const redirection: any = {
    'delete' : {
      title: 'You will be missed ;(',
      subtitle: `Your account shall be permanently deleted in 14 days.
        If you change your mind, please send us a request mail at admin@gmail.com
        and we shall set-up everything just like it was before.. `
    },
    'deactivate' : {
      title: 'You will be missed ;(',
      subtitle: `Whenever you wish to reactivate your account,
      please send us a request mail at admin@gmail.com and we shall set-up
      everything just like it was before.`
    }
  }
  useEffect(() => {
    const fragment = window.location.hash.substring(1);
    if (fragment && redirection[fragment]) {
      setContext(redirection[fragment]);
    }

    setTimeout(() => {
      window.open('/', '_self')
    }, 3000);
  }, []);

  return (
    <div className="message-container width-100 height-100">
      <p className="font-bold width-100 text-center heading-1">{context.title}</p>
      <p className="font-sm text-center width-100 heading-3">
        {context.subtitle}
      </p>
    </div>
  );
};

export default SignOut;
