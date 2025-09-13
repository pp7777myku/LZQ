async function fetchJSON(url, options = {}) {
  const res = await fetch(url, Object.assign({headers: {"Content-Type": "application/json"}}, options));
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

async function loadOverdue() {
  const data = await fetchJSON("/api/overdue");
  const tbody = document.querySelector("#tbl-overdue tbody");
  tbody.innerHTML = "";
  data.forEach(x => {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${x.user_name}</td><td>${x.user_email}</td><td>${x.book_title}</td><td>${x.due_date}</td><td>${x.days_overdue}</td>`;
    tbody.appendChild(tr);
  });
}

async function loadBorrows() {
  const data = await fetchJSON("/api/borrows");
  const tbody = document.querySelector("#tbl-borrows tbody");
  tbody.innerHTML = "";
  data.forEach(x => {
    const status = x.returned ? `已归还（${x.return_date || ""}）` : "未归还";
    const btn = x.returned ? "" : `<button data-id="${x.id}" class="btn-return">标记归还</button>`;
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${x.id}</td><td>${x.user.name}(${x.user.email})</td><td>${x.book.title}</td>
                    <td>${x.borrow_date}</td><td>${x.due_date}</td><td>${status}</td><td>${btn}</td>`;
    tbody.appendChild(tr);
  });

  tbody.querySelectorAll(".btn-return").forEach(btn=>{
    btn.addEventListener("click", async (e)=>{
      const id = e.target.getAttribute("data-id");
      await fetchJSON("/api/borrows/return", {method:"POST", body: JSON.stringify({id: Number(id)})});
      await loadBorrows(); await loadOverdue();
    });
  });
}

document.getElementById("btn-refresh").addEventListener("click", async ()=>{
  await loadOverdue(); await loadBorrows();
});

document.getElementById("btn-notify").addEventListener("click", async ()=>{
  const res = await fetchJSON("/api/notify/run", {method: "POST", body: JSON.stringify({})});
  document.getElementById("notify-result").textContent =
    `已发现 ${res.total_overdues} 条逾期记录，成功发送 ${res.sent} 封邮件（邮件开关：${res.mail_enabled ? "开启" : "关闭"}）`;
  await loadBorrows(); await loadOverdue();
});

document.getElementById("form-user").addEventListener("submit", async (e)=>{
  e.preventDefault();
  const f = e.target;
  await fetchJSON("/api/users", {method:"POST", body: JSON.stringify({
    name: f.name.value.trim(), email: f.email.value.trim(), phone: f.phone.value.trim()
  })});
  f.reset();
  alert("已添加用户");
});

document.getElementById("form-book").addEventListener("submit", async (e)=>{
  e.preventDefault();
  const f = e.target;
  await fetchJSON("/api/books", {method:"POST", body: JSON.stringify({
    title: f.title.value.trim(), author: f.author.value.trim(), isbn: f.isbn.value.trim()
  })});
  f.reset();
  alert("已添加图书");
});

document.getElementById("form-borrow").addEventListener("submit", async (e)=>{
  e.preventDefault();
  const f = e.target;
  await fetchJSON("/api/borrows", {method:"POST", body: JSON.stringify({
    user_id: Number(f.user_id.value), book_id: Number(f.book_id.value),
    borrow_date: f.borrow_date.value, due_date: f.due_date.value
  })});
  f.reset();
  await loadBorrows(); await loadOverdue();
  alert("已登记借阅");
});

(async function init(){
  await loadOverdue();
  await loadBorrows();
})();
