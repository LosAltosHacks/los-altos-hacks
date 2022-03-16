import React, { useEffect, useState } from "react";
import ReactLoading from "react-loading";
import "bootstrap/dist/css/bootstrap.min.css";

import DateAndClock from "./Components/DateAndClock/DateAndClock";
import Faq from "./Components/Faq/Faq";
import HackIsback from "./Components/HackIsback/HackIsback";
import HeroSection from "./Components/HeroSection/HeroSection";
import JudgeAndSpeaker from "./Components/JudgeAndSpeaker/JudgeAndSpeaker";
import Navbar from "./Components/Navbar/Navbar";
import SpecialThanks from "./Components/SpecialThanks/SpecialThanks";
import styled from "styled-components";
const Wrapper = styled.div`
  background: url(/images/background.png);
  background-repeat: no-repeat;
  background-size: cover;
  background-position: top;
  .loader {
    position: fixed;
    width: 100%;
    height: 100%;
    background: #000;
    display: flex;
    justify-content: center;
    align-items: center;
  }
`;
function App() {
  const [loader, setLoader] = useState(false);
  useEffect(() => {
    setLoader(true);
  }, []);

  return (
    <Wrapper>
      {loader ? (
        <>
          <Navbar />
          <HeroSection />
          <HackIsback />
          <DateAndClock />
          <Faq />
          <JudgeAndSpeaker />
          <SpecialThanks />
        </>
      ) : (
        <div className="loader">
          <ReactLoading type="spin" color="#fff" height={100} width={100} />
        </div>
      )}
    </Wrapper>
  );
}

export default App;
