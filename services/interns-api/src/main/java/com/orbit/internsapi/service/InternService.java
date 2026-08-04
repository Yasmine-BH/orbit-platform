package com.orbit.internsapi.service;

import com.orbit.internsapi.dto.CreateInternRequest;
import com.orbit.internsapi.dto.InternResponse;
import com.orbit.internsapi.dto.UpdateInternRequest;
import com.orbit.internsapi.entity.Intern;
import com.orbit.internsapi.exception.DuplicateEmailException;
import com.orbit.internsapi.exception.InternNotFoundException;
import com.orbit.internsapi.repository.InternRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@Transactional
public class InternService {

    private final InternRepository internRepository;

    public InternService(InternRepository internRepository) {
        this.internRepository = internRepository;
    }

    public InternResponse create(CreateInternRequest request) {
        if (internRepository.existsByEmail(request.email())) {
            throw new DuplicateEmailException(request.email());
        }
        Intern intern = new Intern(
                request.firstName(),
                request.lastName(),
                request.email(),
                request.university(),
                request.startDate(),
                request.status()
        );
        return InternResponse.from(internRepository.save(intern));
    }

    @Transactional(readOnly = true)
    public List<InternResponse> findAll() {
        return internRepository.findAll().stream()
                .map(InternResponse::from)
                .toList();
    }

    @Transactional(readOnly = true)
    public InternResponse findById(Long id) {
        return InternResponse.from(getOrThrow(id));
    }

    @Transactional(readOnly = true)
    public boolean existsById(Long id) {
        return internRepository.existsById(id);
    }

    public InternResponse update(Long id, UpdateInternRequest request) {
        Intern intern = getOrThrow(id);

        if (!intern.getEmail().equals(request.email())
                && internRepository.existsByEmail(request.email())) {
            throw new DuplicateEmailException(request.email());
        }

        intern.setFirstName(request.firstName());
        intern.setLastName(request.lastName());
        intern.setEmail(request.email());
        intern.setUniversity(request.university());
        intern.setStartDate(request.startDate());
        intern.setStatus(request.status());

        return InternResponse.from(intern);
    }

    public void delete(Long id) {
        Intern intern = getOrThrow(id);
        internRepository.delete(intern);
    }

    private Intern getOrThrow(Long id) {
        return internRepository.findById(id)
                .orElseThrow(() -> new InternNotFoundException(id));
    }
}
