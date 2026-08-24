(() => {
  const scriptUrl = document.currentScript?.src || window.location.href;
  const wallets = [
    {
      id: "bitcoin",
      name: "Bitcoin",
      ticker: "BTC",
      network: "Bitcoin network",
      address: "bc1q36mmf5s6mpmy7d0v5vttj4c4m32djkmucdsllr",
      qr: "assets/support/qr-bitcoin.png",
    },
    {
      id: "ethereum",
      name: "Ethereum",
      ticker: "ETH",
      network: "Ethereum network",
      address: "0x08533e9E091552f16170dA06E8b882e75b0988Ca",
      qr: "assets/support/qr-ethereum.png",
    },
    {
      id: "usdt",
      name: "USDT",
      ticker: "TRC20",
      network: "TRON network",
      address: "TH8yji4c6db6BeMeVemD4gWhdjaxjnXpyJ",
      qr: "assets/support/qr-usdt-trc20.png",
    },
    {
      id: "gram",
      name: "Gram",
      ticker: "GRAM",
      network: "TON network",
      address: "UQBHA6t2wv6eqikOaOwu_zdC8XzakUjrjTj4UIfRJGje_T_Z",
      qr: "assets/support/qr-gram-ton.png",
    },
  ];

  const iconMarkup = {
    bitcoin: `
      <svg viewBox="0 0 40 40" role="img" aria-label="Bitcoin">
        <circle cx="20" cy="20" r="19" fill="#f7931a" />
        <text x="20" y="27" fill="#fff" font-family="Arial, sans-serif" font-size="22" font-weight="800" text-anchor="middle" transform="rotate(12 20 20)">₿</text>
      </svg>`,
    ethereum: `<img src="${new URL("assets/support/icon-ethereum.svg", scriptUrl).href}" alt="" />`,
    usdt: `<img src="${new URL("assets/support/icon-usdt.svg", scriptUrl).href}" alt="" />`,
    gram: `<img src="${new URL("assets/support/icon-gram.svg", scriptUrl).href}" alt="" />`,
  };

  const shortAddress = (address) => `${address.slice(0, 8)}…${address.slice(-6)}`;

  document.querySelectorAll("[data-wallet-list]").forEach((list) => {
    wallets.forEach((wallet) => {
      const item = document.createElement("div");
      item.className = "development-support-wallet-item";

      const copyButton = document.createElement("button");
      copyButton.type = "button";
      copyButton.className = "development-support-option development-support-copy";
      copyButton.dataset.walletAddress = wallet.address;
      copyButton.dataset.copiedLabel = list.dataset.copiedLabel || "Copied";
      copyButton.dataset.copyFailedLabel = list.dataset.copyFailedLabel || "Copy failed";
      copyButton.setAttribute(
        "aria-label",
        `${list.dataset.copyLabel || "Copy"} ${wallet.name} (${wallet.ticker}, ${wallet.network})`,
      );

      const icon = document.createElement("span");
      icon.className = `development-support-wallet-icon is-${wallet.id}`;
      icon.innerHTML = iconMarkup[wallet.id];

      const details = document.createElement("span");
      details.className = "development-support-wallet";

      const name = document.createElement("span");
      name.className = "development-support-wallet-name";
      name.textContent = `${wallet.name} · ${wallet.ticker}`;

      const address = document.createElement("code");
      address.textContent = shortAddress(wallet.address);

      const action = document.createElement("span");
      action.className = "development-support-copy-action";
      action.textContent = list.dataset.copyLabel || "Copy";

      details.append(name, address);
      copyButton.append(icon, details, action);

      const qrButton = document.createElement("button");
      qrButton.type = "button";
      qrButton.className = "development-support-qr-toggle";
      qrButton.dataset.qrToggle = wallet.id;
      qrButton.setAttribute("aria-expanded", "false");
      qrButton.setAttribute("aria-controls", `support-qr-${wallet.id}`);
      qrButton.setAttribute(
        "aria-label",
        `${list.dataset.showQrLabel || "Show QR code"}: ${wallet.name} (${wallet.network})`,
      );
      qrButton.title = list.dataset.showQrLabel || "Show QR code";
      qrButton.innerHTML = `
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="M4 4h6v6H4zm10 0h6v6h-6zM4 14h6v6H4zm11 0h2v2h-2zm3 0h2v4h-2zm-4 4h4v2h-4z" />
        </svg>
        <span>QR</span>`;

      const qrPanel = document.createElement("div");
      qrPanel.id = `support-qr-${wallet.id}`;
      qrPanel.className = "development-support-qr-panel";
      qrPanel.hidden = true;

      const qrImage = document.createElement("img");
      qrImage.src = new URL(wallet.qr, scriptUrl).href;
      qrImage.width = 236;
      qrImage.height = 236;
      qrImage.loading = "lazy";
      qrImage.alt = `${wallet.name} ${list.dataset.qrCodeLabel || "QR code"}`;

      const qrDetails = document.createElement("div");
      qrDetails.className = "development-support-qr-details";

      const qrNetwork = document.createElement("strong");
      qrNetwork.textContent = `${wallet.name} · ${wallet.network}`;

      const qrInstruction = document.createElement("span");
      qrInstruction.textContent = list.dataset.qrInstruction || "Scan in a compatible wallet, then verify the network and address.";

      const fullAddress = document.createElement("code");
      fullAddress.textContent = wallet.address;

      qrDetails.append(qrNetwork, qrInstruction, fullAddress);
      qrPanel.append(qrImage, qrDetails);
      item.append(copyButton, qrButton, qrPanel);
      list.appendChild(item);
    });
  });

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

  document.querySelectorAll("[data-wallet-address]").forEach((button) => {
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

  document.querySelectorAll("[data-qr-toggle]").forEach((button) => {
    button.addEventListener("click", () => {
      const panel = document.getElementById(button.getAttribute("aria-controls"));
      if (!panel) return;

      const willOpen = panel.hidden;
      button.closest("[data-wallet-list]")?.querySelectorAll("[data-qr-toggle]").forEach((otherButton) => {
        const otherPanel = document.getElementById(otherButton.getAttribute("aria-controls"));
        otherButton.setAttribute("aria-expanded", "false");
        otherButton.classList.remove("is-open");
        if (otherPanel) otherPanel.hidden = true;
      });

      if (willOpen) {
        panel.hidden = false;
        button.setAttribute("aria-expanded", "true");
        button.classList.add("is-open");
      }
    });
  });
})();
