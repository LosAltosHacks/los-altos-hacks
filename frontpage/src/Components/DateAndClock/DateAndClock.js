import React, { useState } from "react";
import { Row, Col } from "react-bootstrap";
import styled from "styled-components";
import Clock from "../Clock/Clock";
const Wrapper = styled.div`
  .main {
    background: linear-gradient(
      180deg,
      rgba(0, 0, 0, 0.57) 0%,
      rgba(0, 0, 0, 0.285) 100%
    );
    border-radius: 70px;
    padding: 35px 40px;
  }
  .day {
    font-family: "Blinker";
    font-style: normal;
    font-weight: 200;
    font-size: 40px;
    line-height: 48px;
    color: #ffffff;
    color: rgba(255, 255, 255, 0.6);
    cursor: pointer;
  }

  .text-container {
    border-bottom: 1px dotted #fff;
  }
  .text {
    font-family: Blinker;
    font-style: normal;
    font-weight: 100;
    font-size: 22px;
    line-height: 48px;
    color: rgba(255, 255, 255, 0.6);
    cursor: pointer;
  }
  .active {
    color: rgba(255, 255, 255, 1);
  }
  .time {
    cursor: pointer;
  }
  @media only screen and (max-width: 991px) {
    .main {
      border-radius: 40px;
      padding: 25px 20px;
    }
  }
`;
const DateAndClock = () => {
  const [time, setTime] = useState(0);
  const [daySelect, setDaySelect] = useState(0);
  const [timeSelect, setTimeSelect] = useState(0);

  const dayArray = ["day 1", "day 2"];
  const dateArray = [
    [
      {
        text: "lorem ipsum",
        timeText: "12:00 am",
        time: "March 19, 1975 24:00:00",
      },
      {
        text: "lorem ipsum",
        timeText: "11:00 pm",
        time: "March 19, 1975 11:00:00",
      },
      {
        text: "lorem ipsum",
        timeText: "09:00 am",
        time: "March 19, 1975 21:00:00",
      },
      {
        text: "lorem ipsum",
        timeText: "12:00 am",
        time: "March 19, 1975 24:00:00",
      },
      {
        text: "lorem ipsum",
        timeText: "11:00 pm",
        time: "March 19, 1975 11:00:00",
      },
      {
        text: "lorem ipsum",
        timeText: "09:00 am",
        time: "March 19, 1975 21:00:00",
      },
      {
        text: "lorem ipsum",
        timeText: "12:00 am",
        time: "March 19, 1975 24:00:00",
      },
    ],
    [
      {
        text: "lorem ipsum",
        timeText: "11:00 am",
        time: "March 19, 1975 24:00:00",
      },
      {
        text: "lorem ipsum",
        timeText: "11:00 pm",
        time: "March 19, 1975 11:00:00",
      },
      {
        text: "lorem ipsum",
        timeText: "09:00 am",
        time: "March 19, 1975 21:00:00",
      },
      {
        text: "lorem ipsum",
        timeText: "12:00 am",
        time: "March 19, 1975 24:00:00",
      },
      {
        text: "lorem ipsum",
        timeText: "11:00 pm",
        time: "March 19, 1975 11:00:00",
      },
      {
        text: "lorem ipsum",
        timeText: "09:00 am",
        time: "March 19, 1975 21:00:00",
      },
      {
        text: "lorem ipsum",
        timeText: "12:00 am",
        time: "March 19, 1975 24:00:00",
      },
    ],
  ];

  return (
    <Wrapper id="schedule">
      <Col
        xs={11}
        sm={9}
        md={10}
        xxl={9}
        className="d-flex flex-column justify-content-center mx-auto"
      >
        <Row className="d-flex justify-content-center ">
          <Col
            md={6}
            lg={5}
            className="d-flex justify-content-center align-items-center flex-column"
          >
            <div className="main w-100 ">
              <div className="dayContainer d-flex justify-content-center pb-3">
                {dayArray.map((el, i) => (
                  <p
                    className={daySelect === i ? "day mx-3 active" : "day mx-3"}
                    key={i}
                    onClick={() => setDaySelect(i)}
                  >
                    {el}
                  </p>
                ))}{" "}
              </div>
              {dateArray[daySelect].map((el, i) => (
                <div
                  className="d-flex justify-content-between w-100 align-items-center text-container"
                  key={i}
                >
                  <p
                    className={timeSelect === i ? "text active" : "text"}
                    key={i}
                    onClick={() => {
                      setTime(i);
                      setTimeSelect(i);
                    }}
                  >
                    {el.text}
                  </p>

                  <p
                    className={
                      timeSelect === i ? "text active text time" : "text time"
                    }
                    onClick={() => {
                      setTime(i);
                      setTimeSelect(i);
                    }}
                  >
                    {el.timeText}
                  </p>
                </div>
              ))}
            </div>
          </Col>
          <Col
            lg={5}
            md={6}
            className="d-flex justify-content-center align-items-center mt-5 my-md-0"
          >
            <Clock time={dateArray[daySelect][time].time} />
          </Col>
        </Row>
      </Col>
    </Wrapper>
  );
};
export default DateAndClock;
