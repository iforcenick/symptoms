import React from 'react'
import Image from 'next/image'

const Header = () => {
    return (
        <div className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm lg:flex">
            <p className="fixed left-0 top-0 flex w-full justify-center bg-gradient-to-b from-zinc-200 pb-6 pt-8 backdrop-blur-2xl dark:border-neutral-800 dark:bg-zinc-800/30 dark:from-inherit lg:static lg:w-auto  lg:rounded-xl lg:border lg:bg-gray-200 lg:p-4 lg:dark:bg-zinc-800/30">
            Probably Genetic Symptom Analysis
            </p>
            <div className="fixed bottom-0 left-0 flex h-48 w-full items-end justify-center bg-gradient-to-t from-white via-white dark:from-black dark:via-black lg:static lg:h-auto lg:w-auto lg:bg-none">
            <span className=" hidden lg:inline">By&nbsp;</span>
            <Image
                src="/logo.jpeg"
                alt="Probably Genetic Logo"
                className="dark:invert"
                width={100}
                height={100}
                priority
            />
            </div>
        </div>
    )
}

export default Header