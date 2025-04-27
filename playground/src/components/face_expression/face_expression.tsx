"use client"
import { useState } from 'react';
import Icon1 from '@/assets/faces/happy.svg';
import Icon2 from '@/assets/faces/sad.svg';
// import { ReactComponent as Icon1 } from '@/assets/faces/happy.svg';
// import { ReactComponent as Icon2 } from '@/assets/faces/sad.svg';


export default function DynamicSvg() {
  const [isToggled, setIsToggled] = useState(false);

  const handleClick = () => setIsToggled(!isToggled);

  return (
    <div>
      <svg xmlns={isToggled ? Icon2 : Icon1}></svg>
    </div>
  );
}