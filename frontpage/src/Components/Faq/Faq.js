import React, { useState } from "react";

import { Col } from "react-bootstrap";

import { BiPlus, BiMinus } from "react-icons/bi";
import styled from "styled-components";

const Wrapper = styled.div`
  padding: 90px 0;
  padding-top: 130px;

  .title {
    font-family: "Avenir";
    font-style: normal;
    font-weight: 300;
    font-size: 80px;
    line-height: 109px;

    color: #ffffff;
  }

  .FaqContainer {
  }
  .question {
    font-family: "Blinker";
    font-style: normal;
    font-weight: 200;
    font-size: 30px;
    line-height: 125%;
    color: #ffffff;
    color: rgba(255, 255, 255, 0.9);
    width: 100%;
    background: rgba(0, 0, 0, 0.33);
    padding: 15px 20px;

    border-radius: 86px;
    width: 100%;
    margin: 15px 0;
  }
  .answer {
    font-family: TT Firs Neue;
    font-style: normal;
    font-weight: normal;
    font-size: 24px;
    line-height: 155%;
    padding: 3px 20px;
    color: rgba(255, 255, 255, 0.9);
  }

  .icon {
    font-size: 25px;
    color: #fff;
    margin-top: 5px;
    margin-left: 10px;
    cursor: pointer;
  }

  @media only screen and (max-width: 1399px) {
    .title {
      font-size: 55px;
    }
  }
  @media only screen and (max-width: 767px) {
    .title {
      font-size: 50px;
    }
    .question {
      font-size: 24px;
      line-height: 150%;
    }
    .answer {
      font-size: 20px;
    }
    .icon {
      font-size: 20px;
      color: #fff;
    }
  }
  @media only screen and (max-width: 520px) {
    .title {
      font-size: 35px;
      line-height: 150%;
    }
  }
`;

const Faq = () => {
  const [value, setValue] = useState(null);
  const dashboardArray = [
    {
      question: "Lorem Ipsum",

      Ans: "Lorem Ipsum",
    },
    {
      question: "Lorem Ipsum",

      Ans: "Lorem Ipsum",
    },
    {
      question: "Lorem Ipsum",

      Ans: "Lorem Ipsum",
    },
    {
      question: "Lorem Ipsum",

      Ans: "Lorem Ipsum",
    },
  ];

  return (
    <Wrapper id="Faq">
      <Col xs={11} md={10} xl={9} xxl={8} className="mx-auto">
        <h3 className="title text-center">faq</h3>

        <div className="pt-4">
          {dashboardArray.map((el, i) => (
            <div key={i} className="FaqContainer">
              <div className="d-flex justify-content-between">
                <div className="question d-flex justify-content-between">
                  {el.question}
                  <div className="d-flFfaqex">
                    {value !== i ? (
                      <BiPlus className="icon" onClick={() => setValue(i)} />
                    ) : (
                      <BiMinus
                        className="icon"
                        onClick={() => setValue(false)}
                      />
                    )}
                  </div>
                </div>
              </div>

              {value === i && <p className="answer">{el.Ans}</p>}
            </div>
          ))}
        </div>
      </Col>
    </Wrapper>
  );
};
export default Faq;
