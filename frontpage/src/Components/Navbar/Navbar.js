import React from 'react';
import { useState } from 'react';
import { Col } from 'react-bootstrap';
import { Link } from 'react-scroll';
import { MdClose } from 'react-icons/md';
import { GiHamburgerMenu } from 'react-icons/gi';
import styled from 'styled-components';
const Wrapper = styled.div`
    position: fixed;
    z-index: 500;
    width: 100%;
    a {
        text-decoration: none;
    }
    .wrapper {
        position: relative;
        padding: 18px 0;
    }

    .changeBackground {
        background: rgba(0, 0, 0, 1);
    }
    .link {
        font-family: 'Blinker';
        font-style: normal;
        font-weight: 200;
        font-size: 35px;
        line-height: 55px;
        cursor: pointer;
        color: #ffffff;
        transition: 0.2s;
    }
    .active {
        font-family: 'Blinker';
        font-style: normal;
        font-weight: 300;
        font-size: 45px;
        line-height: 120%;
        color: #ffffff;
        text-shadow: 0px 8px 40px #ffffff;
        transition: 0.2s;
    }
    .sidebar {
        position: absolute;
        width: 100%;
        top: 0;
        left: 0;
        background: rgba(0, 0, 0, 1);
        padding: 30px 0;
        padding-top: 100px;
        display: flex;
        flex-direction: column;
        ]justify-content: center;
        align-items: center;
    }
    .icon {
        position: absolute;
        right: 5%;
        top: 5%;
        color: #fff;
        font-size: 34px;
    }
    .show {
        max-height: 1000;
    }
    .show .link {
        height: auto;
    }
    .hide .link {
        height: 0;
        overflow: hidden;
    }
    .hide {
        max-height: 0px;
        overflow: hidden;
    }

    @media only screen and (max-width: 1500px) {
        .link {
            font-size: 30px;
        }
    }
`;
const Navbar = () => {
    const [navbar, setNavbar] = useState(false);
    const [sidebar, setSidebar] = useState(false);
    const [value, setValue] = useState(2);
    const changeBackground = () => {
        if (window.scrollY >= 80) {
            setNavbar(true);
            setValue(null);
        } else {
            setNavbar(false);
            setValue(2);
        }
    };

    const navbarArray = [
        { name: 'schedule', to: 'schedule' },
        { name: 'faq', to: 'Faq' },
        { name: 'REGISTER', to: 'register' },
        { name: 'team', to: 'team' },
        { name: 'sponsors', to: 'sponsors' },
    ];
    window.addEventListener('scroll', changeBackground);
    return (
        <Wrapper>
            <div className={navbar ? 'changeBackground wrapper' : 'wrapper'}>
                <Col
                    xs={11}
                    md={10}
                    xl={9}
                    xxl={8}
                    className="d-flex flex-column justify-content-center mx-auto "
                >
                    <div className="d-flex justify-content-end d-md-block">
                        <div className="d-none d-md-flex justify-content-between align-items-center">
                            {navbarArray.map((el, i) => (
                                <Link
                                    key={i}
                                    spy={true}
                                    smooth={true}
                                    offset={50}
                                    duration={500}
                                    to={el.to}
                                    activeClass="active"
                                    className={
                                        value === i ? 'link active' : 'link'
                                    }
                                >
                                    {el.name}
                                </Link>
                            ))}
                        </div>
                        <GiHamburgerMenu
                            className={sidebar ? 'd-none' : 'd-md-none '}
                            color="#fff"
                            size={26}
                            onClick={() => setSidebar(true)}
                        />
                        <div
                            className={
                                sidebar ? 'sidebar show' : 'sidebar hide p-0'
                            }
                        >
                            {navbarArray.map((el, i) => (
                                <Link
                                    key={i}
                                    spy={true}
                                    smooth={true}
                                    offset={50}
                                    duration={500}
                                    to={el.to}
                                    activeClass="active"
                                    className="link py-2"
                                    onClick={() => setSidebar(false)}
                                >
                                    {el.name}
                                </Link>
                            ))}
                            <MdClose
                                className="icon d-block d-md-none "
                                onClick={() => setSidebar(false)}
                            />
                        </div>
                    </div>
                </Col>
            </div>
        </Wrapper>
    );
};
export default Navbar;
