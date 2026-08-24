(() => {
  const wallets = [
    {
      name: "Bitcoin",
      network: "BTC",
      address: "bc1q36mmf5s6mpmy7d0v5vttj4c4m32djkmucdsllr",
    },
    {
      name: "Ethereum",
      network: "ETH",
      address: "0x08533e9E091552f16170dA06E8b882e75b0988Ca",
    },
    {
      name: "USDT",
      network: "TRC20",
      address: "TH8yji4c6db6BeMeVemD4gWhdjaxjnXpyJ",
    },
    {
      name: "TON",
      network: "TON",
      address: "UQBHA6t2wv6eqikOaOwu_zdC8XzakUjrjTj4UIfRJGje_T_Z",
    },
  ];

  const shortAddress = (address) => `${address.slice(0, 8)}…${address.slice(-6)}`;

  document.querySelectorAll("[data-wallet-list]").forEach((list) => {
    wallets.forEach((wallet) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "development-support-option development-support-copy";
      button.dataset.walletAddress = wallet.address;
      button.dataset.copiedLabel = list.dataset.copiedLabel || "Copied";
      button.dataset.copyFailedLabel = list.dataset.copyFailedLabel || "Copy failed";
      button.setAttribute(
        "aria-label",
        `${list.dataset.copyLabel || "Copy"} ${wallet.name} (${wallet.network})`,
      );

      const details = document.createElement("span");
      details.className = "development-support-wallet";

      const name = document.createElement("span");
      name.className = "development-support-wallet-name";
      name.textContent = `${wallet.name} · ${wallet.network}`;

      const address = document.createElement("code");
      address.textContent = shortAddress(wallet.address);

      const action = document.createElement("span");
      action.className = "development-support-copy-action";
      action.textContent = list.dataset.copyLabel || "Copy";

      details.append(name, address);
      button.append(details, action);
      list.appendChild(button);
    });
  });

  const buttons = document.querySelectorAll("[data-wallet-address]");
  if (!buttons.length) return;

  const fallbackCopy = (value) => {
    const input = document.createElement("textarea");
    input.value = value;
    input.setAttribute("readonly", "");
    input.style.position = "fixed";
    input.style.opacity = "0";
    document.body.appendChild(input);
    input.select();
    const copied = document.execCommand("copy");
    input.remove();
    if (!copied) throw new Error("Copy failed");
  };

  buttons.forEach((button) => {
    button.addEventListener("click", async () => {
      const address = button.dataset.walletAddress;
      const action = button.querySelector(".development-support-copy-action");
      if (!address || !action) return;

      const originalLabel = action.textContent;
      try {
        if (navigator.clipboard?.writeText) {
          await navigator.clipboard.writeText(address);
        } else {
          fallbackCopy(address);
        }

        action.textContent = button.dataset.copiedLabel || "Copied";
        button.classList.add("is-copied");
        window.setTimeout(() => {
          action.textContent = originalLabel;
          button.classList.remove("is-copied");
        }, 1800);
      } catch {
        action.textContent = button.dataset.copyFailedLabel || "Copy failed";
        window.setTimeout(() => {
          action.textContent = originalLabel;
        }, 2200);
      }
    });
  });
})();
