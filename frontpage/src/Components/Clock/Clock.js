import React from 'react';
import styled from 'styled-components';
const Wrapper = styled.div`
    font-family: 'Blinker';
    .clock {
        width: 450px;
        height: 450px;
        border-radius: 50%;

        box-shadow: 0 2px 30px rgba(0, 0, 0, 0.2);
        font-size: 24px;
        color: #fff;
        text-align: center;
        position: relative;

        background: rgba(0, 0, 0, 0.2);
    }

    .clock::after {
        background: #fff;
        content: '';
        width: 12px;
        height: 12px;
        border-radius: 50%;
        position: absolute;
        z-index: 2;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        border: 2px solid #fff;
    }

    .hour_hand {
        position: absolute;
        width: 6px;
        height: 140px;
        background: #ffffff;
        top: 19%;
        left: 49.4%;
        transform-origin: bottom;
    }

    .min_hand {
        position: absolute;
        width: 4px;
        height: 80px;
        background: #444;
        top: 22.5%;
        left: 49%;
        transform-origin: bottom;
    }

    .sec_hand {
        position: absolute;
        width: 2px;
        height: 118px;
        background: red;
        top: 10.5%;
        left: 50%;
        transform-origin: bottom;
    }

    .clock span {
        position: absolute;
        font-family: 'Source Sans Pro', sans-serif;
        font-weight: 700;
    }

    .twelve {
        top: 10px;
        left: 46%;
    }

    .one {
        top: 10%;
        right: 26%;
    }

    .eleven {
        top: 10%;
        left: 26%;
    }

    .two {
        top: 25%;
        right: 10%;
    }

    .three {
        right: 10px;
        top: 46%;
    }

    .four {
        right: 30px;
        top: 67%;
    }

    .five {
        right: 78px;
        top: 80%;
    }

    .six {
        bottom: 10px;
        left: 50%;
    }

    .seven {
        left: 80px;
        top: 82%;
    }

    .eight {
        left: 30px;
        top: 67%;
    }

    .nine {
        left: 10px;
        top: 46%;
    }

    .ten {
        top: 25%;
        left: 10%;
    }
    @media only screen and (max-width: 1650px) {
        .clock {
            width: 400px;
            height: 400px;
        }

        .hour_hand {
            height: 110px;

            top: 22.6%;
            left: 49.4%;
        }
    }
    @media only screen and (max-width: 1399px) {
        .clock {
            width: 350px;
            height: 350px;
        }
        .hour_hand {
            height: 100px;

            top: 21.6%;
            left: 49%;
        }
    }
    @media only screen and (max-width: 1199px) {
        .clock {
            width: 300px;
            height: 300px;
        }
        .hour_hand {
            height: 90px;

            top: 20%;
            left: 49%;
        }
    }
    @media only screen and (max-width: 767px) {
        .clock {
            width: 400px;
            height: 400px;
        }
        .hour_hand {
            height: 110px;

            top: 22.6%;
            left: 49.4%;
        }
    }
    @media only screen and (max-width: 575px) {
        .clock {
            width: 350px;
            height: 350px;
        }
        .hour_hand {
            height: 100px;

            top: 21.6%;
            left: 49%;
        }
    }
    @media only screen and (max-width: 420px) {
        .clock {
            width: 300px;
            height: 300px;
        }
        .hour_hand {
            height: 90px;

            top: 20%;
            left: 49%;
        }
    }
`;

const Clock = ({ time }) => {
    return (
        <Wrapper>
            <div className="clock">
                <div
                    className="hour_hand"
                    style={{
                        transform: `rotateZ(${new Date(time).getHours() *
                            30}deg)`,
                    }}
                ></div>

                <span className="twelve">12</span>
                <span className="one"></span>
                <span className="two"></span>
                <span className="three">3</span>
                <span className="four"></span>
                <span className="five"></span>
                <span className="six">6</span>
                <span className="seven"></span>
                <span className="eight"></span>
                <span className="nine">9</span>
                <span className="ten"></span>
                <span className="eleven"></span>
            </div>
        </Wrapper>
    );
};

export default Clock;
