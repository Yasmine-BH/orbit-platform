package com.orbit.internsapi.repository;

import com.orbit.internsapi.entity.Intern;
import org.springframework.data.jpa.repository.JpaRepository;

public interface InternRepository extends JpaRepository<Intern, Long> {

    boolean existsByEmail(String email);
}
