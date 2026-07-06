// ... existing code ...

export const adminLogin = async (req, res) => {
  const { email, password } = req.body;
  try {
    const admin = await Admin.findOne({ email });
    if (!admin) return res.status(404).json({ message: "Admin not found" });

    // Password check (Bcrypt usage check)
    const isMatch = await bcrypt.compare(password, admin.password);
    if (!isMatch) return res.status(400).json({ message: "Invalid credentials" });

    const token = jwt.sign({ id: admin._id, role: 'admin' }, process.env.JWT_SECRET, { expiresIn: '1h' });
    res.status(200).json({ token, admin: { id: admin._id, name: admin.name } });
  } catch (err) {
    res.status(500).json({ message: "Server error", error: err.message });
  }
};

// ... rest of code ...